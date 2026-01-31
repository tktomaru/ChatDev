"""Codex CLI provider implementation.

This provider uses the `codex exec` CLI command to process requests non-interactively.
The prompt is passed via stdin using '-' argument.

Usage in YAML:
  config:
    provider: codex_cli
    name: codex
    role: "System prompt here"
    params:
      timeout: 600
      skip_permissions: true
      sandbox: workspace-write  # read-only, workspace-write, danger-full-access
      model: o3  # optional model override
      json_output: false  # output as JSONL
"""

import json
import subprocess
import shutil
from typing import Any, Dict, List, Optional

from entity.messages import (
    Message,
    MessageRole,
)
from entity.tool_spec import ToolSpec
from runtime.node.agent.providers.base import ModelProvider
from runtime.node.agent.providers.response import ModelResponse
from utils.token_tracker import TokenUsage


class CodexCLIProvider(ModelProvider):
    """Codex CLI provider implementation using the `codex` command."""

    DEFAULT_TIMEOUT = 600  # 10 minutes default timeout

    def create_client(self) -> Dict[str, Any]:
        """Verify that the codex CLI is available and return config."""
        codex_path = shutil.which("codex")
        if not codex_path:
            raise RuntimeError(
                "Codex CLI not found. Please install Codex CLI first.\n"
                "See: https://openai.github.io/codex/"
            )

        working_directory = self.params.get("working_directory")
        if not working_directory:
            workspace_root = getattr(self.config, "workspace_root", None)
            if workspace_root:
                working_directory = str(workspace_root)

        return {
            "codex_path": codex_path,
            "timeout": self.params.get("timeout", self.DEFAULT_TIMEOUT),
            "skip_permissions": self.params.get("skip_permissions", False),
            "sandbox": self.params.get("sandbox", "workspace-write"),
            "full_auto": self.params.get("full_auto", False),
            "json_output": self.params.get("json_output", False),
            "model": self.params.get("model"),
            "working_directory": working_directory,
        }

    def call_model(
        self,
        client: Dict[str, Any],
        conversation: List[Message],
        timeline: List[Any],
        tool_specs: Optional[List[ToolSpec]] = None,
        **kwargs,
    ) -> ModelResponse:
        """Call the Codex CLI with the given messages using 'codex exec'."""
        try:
            # Extract prompts from conversation
            system_prompt, user_prompt = self._extract_prompts(conversation)

            if not user_prompt or not user_prompt.strip():
                user_prompt = "Please respond."

            # Combine prompts
            combined_prompt = user_prompt
            if system_prompt and system_prompt.strip():
                combined_prompt = f"<system>{system_prompt}</system>\n\n{user_prompt}"

            # Build command using 'codex exec' for non-interactive mode
            args = [client["codex_path"], "exec"]

            # Add sandbox mode
            sandbox = client.get("sandbox", "workspace-write")
            if sandbox:
                args.extend(["--sandbox", sandbox])

            # Add permission bypass if requested (overrides sandbox)
            if client.get("skip_permissions"):
                args.append("--dangerously-bypass-approvals-and-sandbox")

            # Add full auto mode if requested
            if client.get("full_auto"):
                args.append("--full-auto")

            # Add model if specified
            model = client.get("model")
            if model:
                args.extend(["--model", model])

            # Add working directory
            working_dir = client.get("working_directory")
            if working_dir:
                args.extend(["--cd", working_dir])

            # Add JSON output if requested
            if client.get("json_output"):
                args.append("--json")

            # Use '-' to read prompt from stdin
            args.append("-")

            # Execute with prompt via stdin
            result = subprocess.run(
                args,
                input=combined_prompt,
                capture_output=True,
                text=True,
                timeout=client.get("timeout", self.DEFAULT_TIMEOUT),
                cwd=working_dir,
            )

            if result.returncode != 0:
                error_msg = f"Codex CLI error (code {result.returncode}): {result.stderr or result.stdout}"
                return ModelResponse(
                    message=Message(
                        role=MessageRole.ASSISTANT,
                        content=error_msg,
                    ),
                    raw_response={
                        "returncode": result.returncode,
                        "stderr": result.stderr,
                        "stdout": result.stdout,
                    },
                )

            # Parse output
            output = result.stdout.strip()
            if client.get("json_output"):
                output = self._parse_json_output(output)

            # Return response
            message = Message(
                role=MessageRole.ASSISTANT,
                content=output,
            )

            return ModelResponse(
                message=message,
                raw_response={
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                },
            )

        except subprocess.TimeoutExpired:
            timeout_val = client.get("timeout", self.DEFAULT_TIMEOUT)
            return ModelResponse(
                message=Message(
                    role=MessageRole.ASSISTANT,
                    content=f"Codex CLI timed out after {timeout_val} seconds.",
                ),
                raw_response={"error": "timeout", "timeout": timeout_val},
            )

        except Exception as e:
            return ModelResponse(
                message=Message(
                    role=MessageRole.ASSISTANT,
                    content=f"Codex CLI execution error: {str(e)}",
                ),
                raw_response={"error": str(e)},
            )

    def extract_token_usage(self, response: Any) -> TokenUsage:
        """Extract token usage from the CLI response."""
        return TokenUsage(
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            metadata={"provider": "codex_cli", "note": "Token usage not available from CLI"},
        )

    def _extract_prompts(self, conversation: List[Message]) -> tuple[Optional[str], str]:
        """Extract system prompt and user prompt from conversation."""
        system_parts = []
        user_parts = []

        for msg in conversation:
            role = msg.role
            content = msg.text_content() if hasattr(msg, 'text_content') else str(msg.content)

            if role == MessageRole.SYSTEM:
                system_parts.append(content)
            elif role == MessageRole.USER:
                user_parts.append(content)
            elif role == MessageRole.ASSISTANT:
                user_parts.append(f"[Previous Response]\n{content}")
            elif role == MessageRole.TOOL:
                user_parts.append(f"[Tool Result]\n{content}")
            else:
                user_parts.append(content)

        system_prompt = "\n\n".join(system_parts) if system_parts else None
        user_prompt = "\n\n".join(user_parts) if user_parts else ""

        return system_prompt, user_prompt

    def _parse_json_output(self, output: str) -> str:
        """Parse JSONL output from Codex CLI and extract message content."""
        messages = []
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                # Extract content from various event types
                if isinstance(data, dict):
                    if "message" in data:
                        messages.append(str(data["message"]))
                    elif "content" in data:
                        messages.append(str(data["content"]))
                    elif "result" in data:
                        messages.append(str(data["result"]))
            except json.JSONDecodeError:
                # If not valid JSON, include the raw line
                messages.append(line)

        return "\n".join(messages) if messages else output

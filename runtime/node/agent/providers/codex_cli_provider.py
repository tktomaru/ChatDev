"""Codex CLI provider implementation.

This provider uses the `codex` CLI command to process requests
instead of making API calls directly.

Usage in YAML:
  config:
    provider: codex_cli
    name: codex  # or other codex models
    role: "System prompt here"
    params:
      timeout: 600
      skip_permissions: true
      output_format: text  # or json, stream-json
"""

import json
import subprocess
import shutil
import tempfile
import os
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
        """
        Verify that the codex CLI is available and return config.

        Returns:
            Dict with CLI configuration
        """
        codex_path = shutil.which("codex")
        if not codex_path:
            raise RuntimeError(
                "Codex CLI not found. Please install Codex CLI first.\n"
                "See: https://docs.anthropic.com/codex"
            )

        # Determine working directory:
        # 1. Explicit param from YAML
        # 2. ChatDev workspace_root from context
        # 3. Current directory (None = subprocess default)
        working_directory = self.params.get("working_directory")
        if not working_directory:
            workspace_root = getattr(self.config, "workspace_root", None)
            if workspace_root:
                working_directory = str(workspace_root)

        return {
            "codex_path": codex_path,
            "timeout": self.params.get("timeout", self.DEFAULT_TIMEOUT),
            "output_format": self.params.get("output_format", "text"),
            "allowedTools": self.params.get("allowedTools", []),
            "disallowedTools": self.params.get("disallowedTools", []),
            "skip_permissions": self.params.get("skip_permissions", False),
            "permission_mode": self.params.get("permission_mode"),
            "verbose": self.params.get("verbose", False),
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
        """
        Call the Codex CLI with the given messages.

        Codex CLI does not support stdin. This implementation writes the prompt
        to a temporary file and passes it as an argument to avoid command line length limits.

        Args:
            client: CLI configuration from create_client()
            conversation: List of messages in the conversation
            timeline: Event timeline (not used for CLI)
            tool_specs: Tool specifications (passed to CLI if supported)
            **kwargs: Additional parameters

        Returns:
            ModelResponse containing the CLI output
        """
        # Extract system prompt and user prompt from conversation
        system_prompt, user_prompt = self._extract_prompts(conversation)

        # Debug: Log conversation contents
        if self.params.get("debug"):
            print(f"[Codex CLI Debug] Conversation has {len(conversation)} messages:")
            for i, msg in enumerate(conversation):
                role = msg.role.value if hasattr(msg.role, 'value') else str(msg.role)
                content = msg.text_content() if hasattr(msg, 'text_content') else str(msg.content)
                print(f"  [{i}] {role}: {content[:200]}...")

        # Ensure we have a prompt
        if not user_prompt or not user_prompt.strip():
            user_prompt = "Please respond based on the system prompt provided."

        # Combine system prompt and user prompt
        combined_prompt = user_prompt
        if system_prompt and system_prompt.strip():
            combined_prompt = f"""<system>
{system_prompt}
</system>

{user_prompt}"""

        if self.params.get("debug"):
            print(f"[Codex CLI Debug] Combined prompt length: {len(combined_prompt)}")

        # Write prompt to temporary file to avoid command line length limits
        # (Windows limit is 8191 characters)
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.txt',
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(combined_prompt)
                temp_file = f.name

            if self.params.get("debug"):
                print(f"[Codex CLI Debug] Prompt written to temporary file: {temp_file}")

            # Execute CLI - read file content and pass directly as argument
            working_dir = client.get("working_directory")
            try:
                # Read the file content
                with open(temp_file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                # Build command with file content
                codex_path = client["codex_path"]
                args = [codex_path]
                
                if client.get("skip_permissions"):
                    args.append("--dangerously-bypass-approvals-and-sandbox")
                if client.get("verbose"):
                    args.append("--verbose")
                
                extra_args = self.params.get("extra_args", [])
                if extra_args:
                    args.extend(extra_args)
                
                args.append(file_content)

                # Debug: Log the command being executed
                if self.params.get("debug"):
                    cmd_display = args[:-1] + [f"[{len(file_content)} chars content]"]
                    print(f"[Codex CLI Debug] Command: {' '.join(cmd_display)}")
                    print(f"[Codex CLI Debug] Working directory: {working_dir}")

                result = subprocess.run(
                    args,
                    capture_output=True,
                    text=True,
                    timeout=client.get("timeout", self.DEFAULT_TIMEOUT),
                    cwd=working_dir,
                )

                stdout = result.stdout
                stderr = result.stderr

                if result.returncode != 0:
                    error_msg = f"Codex CLI error (code {result.returncode}): {stderr or stdout}"
                    return ModelResponse(
                        message=Message(
                            role=MessageRole.ASSISTANT,
                            content=error_msg,
                        ),
                        raw_response={"returncode": result.returncode, "stderr": stderr, "stdout": stdout},
                    )

                # Parse output based on format
                output_format = client.get("output_format", "text")
                if output_format == "json":
                    response_content = self._parse_json_output(stdout)
                else:
                    response_content = stdout.strip()

                message = Message(
                    role=MessageRole.ASSISTANT,
                    content=response_content,
                )

                return ModelResponse(
                    message=message,
                    raw_response={"stdout": stdout, "stderr": stderr, "returncode": result.returncode},
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

        finally:
            # Clean up temporary file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                    if self.params.get("debug"):
                        print(f"[Codex CLI Debug] Temporary file cleaned up: {temp_file}")
                except Exception as e:
                    if self.params.get("debug"):
                        print(f"[Codex CLI Debug] Warning: Failed to clean up temp file: {e}")

    def extract_token_usage(self, response: Any) -> TokenUsage:
        """
        Extract token usage from the CLI response.

        Note: CLI doesn't provide token usage, so we return empty usage.

        Args:
            response: Raw response from CLI

        Returns:
            Empty TokenUsage instance
        """
        return TokenUsage(
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            metadata={"provider": "codex_cli", "note": "Token usage not available from CLI"},
        )

    def _extract_prompts(self, conversation: List[Message]) -> tuple[Optional[str], str]:
        """
        Extract system prompt and user prompt from conversation.

        Args:
            conversation: List of messages

        Returns:
            Tuple of (system_prompt, user_prompt)
        """
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
                user_parts.append(f"[Previous Assistant Response]\n{content}")
            elif role == MessageRole.TOOL:
                user_parts.append(f"[Tool Result]\n{content}")
            else:
                user_parts.append(content)

        system_prompt = "\n\n".join(system_parts) if system_parts else None
        user_prompt = "\n\n".join(user_parts) if user_parts else ""

        return system_prompt, user_prompt

    def _parse_json_output(self, output: str) -> str:
        """
        Parse JSON output from CLI.

        Args:
            output: Raw CLI output

        Returns:
            Extracted content or raw output if parsing fails
        """
        try:
            data = json.loads(output)
            # Extract content based on common JSON structures
            if isinstance(data, dict):
                if "content" in data:
                    return data["content"]
                if "result" in data:
                    return data["result"]
                if "message" in data:
                    return data["message"]
            return output
        except json.JSONDecodeError:
            return output

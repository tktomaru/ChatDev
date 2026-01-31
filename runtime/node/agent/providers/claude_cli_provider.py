"""Claude CLI provider implementation.

This provider uses the `claude` CLI command (Claude Code) to process requests
instead of making API calls directly.

Usage in YAML:
  config:
    provider: claude_cli
    name: sonnet  # or opus, haiku, claude-sonnet-4-5-20250929, etc.
    role: "System prompt here"
    params:
      timeout: 600
      skip_permissions: true
      allowedTools:
        - Bash
        - Read
        - Write
        - Edit
      output_format: text  # or json, stream-json
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


class ClaudeCLIProvider(ModelProvider):
    """Claude CLI provider implementation using the `claude` command."""

    DEFAULT_TIMEOUT = 600  # 10 minutes default timeout

    def create_client(self) -> Dict[str, Any]:
        """
        Verify that the claude CLI is available and return config.

        Returns:
            Dict with CLI configuration
        """
        claude_path = shutil.which("claude")
        if not claude_path:
            raise RuntimeError(
                "Claude CLI not found. Please install Claude Code CLI first.\n"
                "See: https://docs.anthropic.com/claude-code"
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
            "claude_path": claude_path,
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
        Call the Claude CLI with the given messages.

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
            print(f"[Claude CLI Debug] Conversation has {len(conversation)} messages:")
            for i, msg in enumerate(conversation):
                role = msg.role.value if hasattr(msg.role, 'value') else str(msg.role)
                content = msg.text_content() if hasattr(msg, 'text_content') else str(msg.content)
                print(f"  [{i}] {role}: {content[:200]}...")
            print(f"[Claude CLI Debug] System prompt length: {len(system_prompt) if system_prompt else 0}")
            print(f"[Claude CLI Debug] System prompt: {system_prompt[:500] if system_prompt else 'None'}...")
            print(f"[Claude CLI Debug] User prompt length: {len(user_prompt) if user_prompt else 0}")
            print(f"[Claude CLI Debug] User prompt: {user_prompt[:500] if user_prompt else 'None'}...")

        # Ensure we have a prompt
        if not user_prompt or not user_prompt.strip():
            user_prompt = "Please respond based on the system prompt provided."

        # Combine system prompt and user prompt into stdin to avoid command line length limits
        # The system prompt is prepended to the user prompt as instructions
        combined_prompt = user_prompt
        if system_prompt and system_prompt.strip():
            combined_prompt = f"""<system>
{system_prompt}
</system>

{user_prompt}"""

        if self.params.get("debug"):
            print(f"[Claude CLI Debug] Combined prompt length: {len(combined_prompt)}")
            print(f"[Claude CLI Debug] Combined prompt (first 800 chars): {combined_prompt[:800]}...")

        # Build CLI command without system prompt (it's included in stdin now)
        cmd = self._build_command(client, None, None)

        # Debug: Log the command being executed
        if self.params.get("debug"):
            # Show command without the full system prompt (too long)
            cmd_display = []
            skip_next = False
            for i, arg in enumerate(cmd):
                if skip_next:
                    skip_next = False
                    cmd_display.append(f"[{len(arg)} chars]")
                elif arg == "--system-prompt":
                    cmd_display.append(arg)
                    skip_next = True
                else:
                    cmd_display.append(arg)
            print(f"[Claude CLI Debug] Command: {' '.join(cmd_display)}")
            print(f"[Claude CLI Debug] Working directory: {client.get('working_directory')}")

        # Execute CLI with combined prompt via stdin for better handling of special characters
        working_dir = client.get("working_directory")
        try:
            result = subprocess.run(
                cmd,
                input=combined_prompt,
                capture_output=True,
                text=True,
                timeout=client.get("timeout", self.DEFAULT_TIMEOUT),
                cwd=working_dir,
            )

            stdout = result.stdout
            stderr = result.stderr

            if result.returncode != 0:
                error_msg = f"Claude CLI error (code {result.returncode}): {stderr or stdout}"
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
                    content=f"Claude CLI timed out after {timeout_val} seconds.",
                ),
                raw_response={"error": "timeout", "timeout": timeout_val},
            )
        except Exception as e:
            return ModelResponse(
                message=Message(
                    role=MessageRole.ASSISTANT,
                    content=f"Claude CLI execution error: {str(e)}",
                ),
                raw_response={"error": str(e)},
            )

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
            metadata={"provider": "claude_cli", "note": "Token usage not available from CLI"},
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

    def _build_command(
        self,
        client: Dict[str, Any],
        system_prompt: Optional[str],
        user_prompt: Optional[str],
    ) -> List[str]:
        """
        Build the CLI command with arguments.

        Args:
            client: CLI configuration
            system_prompt: System prompt (optional)
            user_prompt: User prompt (optional - if None, prompt is passed via stdin)

        Returns:
            Command as list of strings
        """
        cmd = [client["claude_path"]]

        # Use print mode for non-interactive execution
        cmd.append("-p")

        # Add permission bypass if requested
        if client.get("skip_permissions"):
            cmd.append("--dangerously-skip-permissions")

        # Add permission mode if specified
        permission_mode = client.get("permission_mode")
        if permission_mode:
            cmd.extend(["--permission-mode", permission_mode])

        # Add system prompt if provided
        if system_prompt:
            cmd.extend(["--system-prompt", system_prompt])

        # Add output format if not text
        output_format = client.get("output_format", "text")
        if output_format and output_format != "text":
            cmd.extend(["--output-format", output_format])

        # Add allowed tools if specified
        allowed_tools = client.get("allowedTools", [])
        if allowed_tools:
            tools_str = ",".join(allowed_tools)
            cmd.extend(["--allowedTools", tools_str])

        # Add disallowed tools if specified
        disallowed_tools = client.get("disallowedTools", [])
        if disallowed_tools:
            tools_str = ",".join(disallowed_tools)
            cmd.extend(["--disallowedTools", tools_str])

        # Add model name if specified
        if self.model_name and self.model_name != "claude":
            cmd.extend(["--model", self.model_name])

        # Add verbose flag
        if client.get("verbose"):
            cmd.append("--verbose")

        # Add any extra CLI arguments from params
        extra_args = self.params.get("extra_args", [])
        if extra_args:
            cmd.extend(extra_args)

        # Add user prompt as positional argument only if provided
        # (otherwise it will be passed via stdin)
        if user_prompt:
            cmd.append(user_prompt)

        return cmd

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

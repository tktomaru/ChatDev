"""Register built-in agent providers."""

from runtime.node.agent.providers.base import ProviderRegistry

from runtime.node.agent.providers.openai_provider import OpenAIProvider

ProviderRegistry.register(
    "openai",
    OpenAIProvider,
    label="OpenAI",
    summary="OpenAI models via the official OpenAI SDK (responses API)",
)

# Claude CLI Provider
try:
    from runtime.node.agent.providers.claude_cli_provider import ClaudeCLIProvider

    ProviderRegistry.register(
        "claude_cli",
        ClaudeCLIProvider,
        label="Claude CLI",
        summary="Claude models via the Claude Code CLI command",
    )
except ImportError:
    print("Claude CLI provider not registered: import error.")

try:
    from runtime.node.agent.providers.gemini_provider import GeminiProvider
except ImportError:
    GeminiProvider = None

if GeminiProvider is not None:
    ProviderRegistry.register(
        "gemini",
        GeminiProvider,
        label="Google Gemini",
        summary="Google Gemini models via google-genai",
    )
else:
    print("Gemini provider not registered: google-genai library not found.")

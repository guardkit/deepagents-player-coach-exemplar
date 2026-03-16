"""Player agent factory for the adversarial cooperation pattern."""

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from prompts.player_prompts import PLAYER_SYSTEM_PROMPT
from tools.search_data import search_data
from tools.write_output import write_output


def create_player(model, domain_prompt: str):
    """Create a configured Player agent instance.

    Args:
        model: The LLM model instance or provider:model string.
        domain_prompt: Domain-specific criteria appended to the system prompt.

    Returns:
        A configured DeepAgent with search and write tools.
    """
    system_prompt = PLAYER_SYSTEM_PROMPT + "\n\n" + domain_prompt
    return create_deep_agent(
        model=model,
        tools=[search_data, write_output],
        system_prompt=system_prompt,
        memory=["./AGENTS.md"],
        backend=FilesystemBackend(root_dir="."),
    )

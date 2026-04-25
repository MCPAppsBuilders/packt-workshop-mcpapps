"""Tests for MCP server prompts: calculate."""

import pytest


class TestCalculatePrompt:
    """Tests for the calculate prompt."""

    async def test_default_prompt(self, mcp):
        result = await mcp.get_prompt("calculate")
        text = result.messages[0].content.text
        assert "add" in text
        assert "a=0" in text
        assert "b=0" in text

    async def test_custom_params(self, mcp):
        result = await mcp.get_prompt(
            "calculate",
            arguments={"operation": "subtract", "a": "10", "b": "3"},
        )
        text = result.messages[0].content.text
        assert "subtract" in text
        assert "a=10" in text
        assert "b=3" in text

    async def test_prompt_returns_user_message(self, mcp):
        result = await mcp.get_prompt("calculate")
        assert result.messages[0].role == "user"


class TestPromptDiscovery:
    """Verify that all expected prompts are registered."""

    async def test_list_prompts(self, mcp):
        prompts = await mcp.list_prompts()
        prompt_names = {p.name for p in prompts}
        assert "calculate" in prompt_names

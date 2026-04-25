"""Tests for MCP server tools: add, add_with_ui, subtract."""

import pytest


class TestAddTool:
    """Tests for the add tool."""

    async def test_add_positive_numbers(self, mcp):
        content, _ = await mcp.call_tool("add", {"a": 2, "b": 3})
        assert content[0].text == "5.0"

    async def test_add_negative_numbers(self, mcp):
        content, _ = await mcp.call_tool("add", {"a": -5, "b": -3})
        assert content[0].text == "-8.0"

    async def test_add_floats(self, mcp):
        content, _ = await mcp.call_tool("add", {"a": 1.5, "b": 2.5})
        assert content[0].text == "4.0"

    async def test_add_zero(self, mcp):
        content, _ = await mcp.call_tool("add", {"a": 0, "b": 0})
        assert content[0].text == "0.0"

    async def test_add_mixed_sign(self, mcp):
        content, _ = await mcp.call_tool("add", {"a": 10, "b": -4})
        assert content[0].text == "6.0"


class TestAddWithUiTool:
    """Tests for the add_with_ui tool (same logic as add)."""

    async def test_add_with_ui_basic(self, mcp):
        content, _ = await mcp.call_tool("add_with_ui", {"a": 7, "b": 8})
        assert content[0].text == "15.0"


class TestSubtractTool:
    """Tests for the subtract tool."""

    async def test_subtract_basic(self, mcp):
        content, _ = await mcp.call_tool("subtract", {"a": 10, "b": 4})
        assert content[0].text == "6.0"

    async def test_subtract_negative_result(self, mcp):
        content, _ = await mcp.call_tool("subtract", {"a": 3, "b": 7})
        assert content[0].text == "-4.0"

    async def test_subtract_floats(self, mcp):
        content, _ = await mcp.call_tool("subtract", {"a": 5.5, "b": 2.2})
        value = float(content[0].text)
        assert abs(value - 3.3) < 1e-9

    async def test_subtract_zero(self, mcp):
        content, _ = await mcp.call_tool("subtract", {"a": 42, "b": 0})
        assert content[0].text == "42.0"


class TestToolDiscovery:
    """Verify that all expected tools are registered."""

    async def test_list_tools(self, mcp):
        tools = await mcp.list_tools()
        tool_names = {t.name for t in tools}
        assert "add" in tool_names
        assert "add_with_ui" in tool_names
        assert "subtract" in tool_names

    async def test_tool_descriptions(self, mcp):
        tools = await mcp.list_tools()
        by_name = {t.name: t for t in tools}
        assert "Add two numbers" in by_name["add"].description
        assert "Subtract" in by_name["subtract"].description

"""Tests for MCP server resources: info.txt, config.json."""

import json


class TestInfoResource:
    """Tests for the file://info.txt resource."""

    async def test_read_info(self, mcp):
        contents = list(await mcp.read_resource("file://info.txt/"))
        text = contents[0].content
        assert len(text) > 0
        assert "MCP" in text

    async def test_info_is_text(self, mcp):
        contents = list(await mcp.read_resource("file://info.txt/"))
        assert contents[0].mime_type is None or "text" in contents[0].mime_type


class TestConfigResource:
    """Tests for the file://config.json resource."""

    async def test_read_config(self, mcp):
        contents = list(await mcp.read_resource("file://config.json/"))
        data = json.loads(contents[0].content)
        assert data["server_name"] == "mcp-basic-server"
        assert data["version"] == "0.1.0"

    async def test_config_operations(self, mcp):
        contents = list(await mcp.read_resource("file://config.json/"))
        data = json.loads(contents[0].content)
        assert "add" in data["supported_operations"]
        assert "subtract" in data["supported_operations"]


class TestResourceDiscovery:
    """Verify that all expected resources are registered."""

    async def test_list_resources(self, mcp):
        resources = await mcp.list_resources()
        uris = {str(r.uri) for r in resources}
        assert "file://info.txt/" in uris
        assert "file://config.json/" in uris

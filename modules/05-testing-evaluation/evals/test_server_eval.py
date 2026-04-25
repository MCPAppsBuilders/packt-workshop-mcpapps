"""End-to-end evaluations for the basic-math MCP server using mcp-eval.

These tests require:
  1. The MCP server running on http://localhost:8301
  2. An ANTHROPIC_API_KEY in the environment (or .env)

Run with:
  mcp-eval run evals/
"""

from mcp_eval import Expect, task, parametrize


@task("Agent should use the add tool to compute 12 + 8")
async def test_addition(agent, session):
    response = await agent.generate_str("What is 12 + 8? Use the available tools to compute this.")
    await session.assert_that(
        Expect.tools.was_called("add"),
        name="addition_tool_called",
        response=response,
    )
    await session.assert_that(
        Expect.content.contains("20"),
        name="addition_result_correct",
        response=response,
    )


@task("Agent should use the subtract tool to compute 25 - 13")
async def test_subtraction(agent, session):
    response = await agent.generate_str("What is 25 minus 13? Use the available tools.")
    await session.assert_that(
        Expect.tools.was_called("subtract"),
        name="subtraction_tool_called",
        response=response,
    )
    await session.assert_that(
        Expect.content.contains("12"),
        name="subtraction_result_correct",
        response=response,
    )


@parametrize(
    "operation,a,b,expected",
    [
        ("add", -15, 7, "-8"),
        ("subtract", 30, 100, "-70"),
    ],
)
@task("Agent should handle negative results correctly")
async def test_negative_results(agent, session, operation, a, b, expected):
    response = await agent.generate_str(
        f"Use the {operation} tool with a={a} and b={b}. What is the result?"
    )
    await session.assert_that(
        Expect.tools.was_called(operation),
        name=f"{operation}_called",
        response=response,
    )
    await session.assert_that(
        Expect.content.contains(expected),
        name=f"{operation}_result_{expected}",
        response=response,
    )


@task("Agent should call add with correct arguments")
async def test_correct_arguments(agent, session):
    response = await agent.generate_str("Add 15 and 27 using the add tool.")
    await session.assert_that(
        Expect.tools.was_called("add"),
        name="add_tool_called",
        response=response,
    )
    await session.assert_that(
        Expect.content.contains("42"),
        name="result_is_42",
        response=response,
    )


@task("All tool calls should succeed")
async def test_tool_success_rate(agent, session):
    response = await agent.generate_str("What is 1 + 1? Use the add tool.")
    await session.assert_that(
        Expect.tools.was_called("add"),
        name="add_called",
        response=response,
    )
    await session.assert_that(
        Expect.content.contains("2"),
        name="result_is_2",
        response=response,
    )

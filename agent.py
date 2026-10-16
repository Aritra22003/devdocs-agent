
import asyncio
import json
import sys
from pathlib import Path

import requests
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

BASE_DIR = Path(__file__).resolve().parent
MODEL = "qwen3:4b"
OLLAMA_URL = "http://localhost:11434/api/chat"


def ask_ollama(messages, tools):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "tools": tools,
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["message"]


def convert_tools(mcp_tools):
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema,
            },
        }
        for tool in mcp_tools
    ]


def result_text(result):
    return "\n".join(
        item.text
        for item in result.content
        if hasattr(item, "text")
    )


async def run_agent(question):
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(BASE_DIR / "server.py")],
        cwd=str(BASE_DIR),
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            discovered = await session.list_tools()
            tools = convert_tools(discovered.tools)

            print("\nMCP tools discovered:")
            for tool in discovered.tools:
                print(f"- {tool.name}")

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DevDocs Agent. Answer questions using "
                        "the local developer documentation. Use search_docs "
                        "when documentation lookup is relevant. Cite the "
                        "returned source filenames. If documentation does "
                        "not contain an answer, say so. Never invent facts."
                    ),
                },
                {"role": "user", "content": question},
            ]

            allowed = {tool.name for tool in discovered.tools}

            for _ in range(5):
                message = await asyncio.to_thread(
                    ask_ollama, messages, tools
                )
                messages.append(message)

                calls = message.get("tool_calls", [])
                if not calls:
                    print("\nDevDocs Agent:\n")
                    print(message.get("content", "No answer returned."))
                    return

                for call in calls:
                    function = call["function"]
                    name = function["name"]
                    arguments = function.get("arguments", {})

                    if name not in allowed:
                        print(f"Blocked unknown tool: {name}")
                        continue

                    if isinstance(arguments, str):
                        arguments = json.loads(arguments)

                    print(f"\n[Calling MCP tool: {name}]")
                    print(f"[Arguments: {arguments}]")

                    result = await session.call_tool(
                        name,
                        arguments=arguments,
                    )

                    messages.append({
                        "role": "tool",
                        "tool_name": name,
                        "content": result_text(result),
                    })

            print("Stopped after five tool-calling rounds.")


def main():
    print("=== DevDocs Agent ===")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        try:
            asyncio.run(run_agent(question))
        except requests.ConnectionError:
            print("Cannot reach Ollama. Check that Ollama is running.")
        except requests.HTTPError as exc:
            print(f"Ollama HTTP error: {exc}")
        except Exception as exc:
            print(f"Error: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()

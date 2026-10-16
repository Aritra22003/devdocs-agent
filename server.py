
from pathlib import Path
from mcp.server.fastmcp import FastMCP

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"

mcp = FastMCP("DevDocs Agent")


@mcp.tool()
def search_docs(query: str) -> str:
    """Search local developer documentation for relevant information."""
    terms = {
        word.lower().strip(".,?!:;()[]{}\"'")
        for word in query.split()
        if len(word.strip(".,?!:;()[]{}\"'")) > 2
    }

    if not terms:
        return "Please provide a more specific search query."

    if not DOCS_DIR.exists():
        return "Documentation folder not found."

    matches = []

    for path in sorted(DOCS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8").lower()
        score = sum(term in content for term in terms)

        if score:
            matches.append((score, path.name, content))

    matches.sort(key=lambda item: item[0], reverse=True)

    if not matches:
        return "No matching documentation found."

    return "\n\n".join(
        f"Source: docs/{name}\n{content}"
        for _, name, content in matches[:3]
    )


if __name__ == "__main__":
    mcp.run()

#!/usr/bin/env python3
"""
Generiert eine HTML-Dokumentation aus den Markdown-Dateien.

Usage:
    python generate_docs.py

Output:
    docs.html - Öffne diese Datei im Browser
"""

import markdown
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "docs"
OUTPUT_FILE = Path(__file__).parent / "docs.html"

# HTML Template mit Mermaid-Support
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IZB Test Suite - Dokumentation</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --bg: #1a1a2e;
            --bg-light: #16213e;
            --text: #eaeaea;
            --accent: #4f8cff;
            --border: #2a2a4a;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .container {{
            display: flex;
            min-height: 100vh;
        }}
        nav {{
            width: 280px;
            background: var(--bg-light);
            padding: 20px;
            border-right: 1px solid var(--border);
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }}
        nav h2 {{
            color: var(--accent);
            margin-top: 0;
            font-size: 1.2em;
        }}
        nav ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        nav li {{
            margin: 8px 0;
        }}
        nav a {{
            color: var(--text);
            text-decoration: none;
            opacity: 0.8;
            transition: opacity 0.2s;
        }}
        nav a:hover {{
            opacity: 1;
            color: var(--accent);
        }}
        main {{
            flex: 1;
            margin-left: 280px;
            padding: 40px 60px;
            max-width: 900px;
        }}
        h1 {{
            color: var(--accent);
            border-bottom: 2px solid var(--border);
            padding-bottom: 10px;
        }}
        h2 {{
            color: var(--accent);
            margin-top: 40px;
        }}
        h3 {{
            color: #7aa2f7;
        }}
        code {{
            background: var(--bg-light);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'SF Mono', Monaco, monospace;
        }}
        pre {{
            background: var(--bg-light);
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid var(--border);
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid var(--border);
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: var(--bg-light);
            color: var(--accent);
        }}
        a {{
            color: var(--accent);
        }}
        .section {{
            margin-bottom: 60px;
            padding-bottom: 40px;
            border-bottom: 1px solid var(--border);
        }}
        .mermaid {{
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <h2>IZB Test Suite</h2>
            <ul>
                <li><a href="#prozess">Prozessübersicht</a></li>
                <li><strong>Skripte:</strong></li>
                {nav_items}
            </ul>
        </nav>
        <main>
            {content}
        </main>
    </div>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</body>
</html>
"""


def convert_mermaid_blocks(html_content: str) -> str:
    """Konvertiert ```mermaid Blöcke zu <div class="mermaid">."""
    import re

    # Pattern für mermaid code blocks (mit oder ohne codehilite class)
    pattern = r'<pre[^>]*><code class="language-mermaid">(.*?)</code></pre>'

    def replace_mermaid(match):
        code = match.group(1)
        # HTML entities zurück konvertieren
        code = code.replace('&gt;', '>')
        code = code.replace('&lt;', '<')
        code = code.replace('&amp;', '&')
        code = code.replace('&quot;', '"')
        return f'<pre class="mermaid">{code}</pre>'

    return re.sub(pattern, replace_mermaid, html_content, flags=re.DOTALL)


def main():
    print("Generiere HTML-Dokumentation...")

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'codehilite', 'toc'])

    content_parts = []
    nav_items = []

    # Prozessübersicht
    process_file = DOCS_DIR / "PROCESS_FLOW.md"
    if process_file.exists():
        process_md = process_file.read_text()
        process_html = md.convert(process_md)
        process_html = convert_mermaid_blocks(process_html)
        content_parts.append(f'<section id="prozess" class="section">{process_html}</section>')
        md.reset()

    # Skript-Dokumentationen
    scripts_dir = DOCS_DIR / "scripts"
    if scripts_dir.exists():
        for md_file in sorted(scripts_dir.glob("*.md")):
            script_name = md_file.stem
            script_id = script_name.replace("_", "-")

            # Navigation
            nav_items.append(f'<li><a href="#{script_id}">{script_name}</a></li>')

            # Content
            script_md = md_file.read_text()
            script_html = md.convert(script_md)
            content_parts.append(f'<section id="{script_id}" class="section">{script_html}</section>')
            md.reset()

    # HTML zusammenbauen
    html = HTML_TEMPLATE.format(
        nav_items="\n                ".join(nav_items),
        content="\n            ".join(content_parts)
    )

    # Speichern
    OUTPUT_FILE.write_text(html)
    print(f"Fertig! Öffne: {OUTPUT_FILE}")
    print(f"Oder: open {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

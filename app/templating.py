"""Shared Jinja2 template engine configuration and safe lesson formatting."""

import html
import re
from pathlib import Path

from fastapi.templating import Jinja2Templates
from markupsafe import Markup

from app.config import get_settings

BASE_APP_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_APP_DIR / "templates"))
templates.env.globals["settings"] = get_settings()


def format_lesson_content(raw_text: str) -> Markup:
    """Safely convert simple markdown (code fences, lists, inline code, paragraphs) to HTML."""
    if not raw_text:
        return Markup("<p class='muted'>Lesson notes are being prepared.</p>")

    parts = re.split(r"```([a-zA-Z0-9_-]*)\n([\s\S]*?)```", raw_text)
    html_out = []

    i = 0
    while i < len(parts):
        text_chunk = parts[i]
        if text_chunk.strip():
            html_out.append(_format_text_blocks(text_chunk))
        if i + 2 < len(parts):
            lang = html.escape(parts[i + 1].strip() or "code")
            code_body = html.escape(parts[i + 2].rstrip())
            html_out.append(
                f'<div class="code-block"><div class="code-block-head">{lang}</div>'
                f"<pre><code>{code_body}</code></pre></div>"
            )
            i += 3
        else:
            i += 1

    return Markup("\n".join(html_out))


def _format_text_blocks(text: str) -> str:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
    rendered = []
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if all(line.lstrip().startswith("- ") for line in lines):
            items = "".join(
                f"<li>{_format_inline(line.lstrip()[2:])}</li>" for line in lines
            )
            rendered.append(f"<ul>{items}</ul>")
        elif all(re.match(r"^\d+\.\s+", line.lstrip()) for line in lines):
            ol_items = []
            for line in lines:
                cleaned = re.sub(r"^\d+\.\s+", "", line.lstrip())
                ol_items.append(f"<li>{_format_inline(cleaned)}</li>")
            rendered.append(f"<ol>{''.join(ol_items)}</ol>")
        else:
            joined = " ".join(_format_inline(line.strip()) for line in lines)
            rendered.append(f"<p>{joined}</p>")
    return "\n".join(rendered)


def _format_inline(line: str) -> str:
    escaped = html.escape(line)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


templates.env.filters["lesson_html"] = format_lesson_content

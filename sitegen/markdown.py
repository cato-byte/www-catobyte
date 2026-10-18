"""Markdown to HTML for blog posts and project pages.

Content conventions (kept from the original blog so old posts render unchanged):
  * The first `#`/`##` heading is the page title. The template renders it as <h1>,
    so it is removed from the body and the remaining headings are shifted to start at <h2>.
  * A heading containing {{PUBLISH_DATE}} is removed; the template shows the date.
  * The image right after `<!-- TITLE_IMAGE -->` is the cover image, also rendered by the template.
  * An image alone in a paragraph becomes a <figure> with its alt text as caption.
  * Study guides: after a `<!-- QA -->` line, every `###` is a category and every `####` a
    question. Each question and its answer become a collapsible <details class="qa"> card; the
    categories are returned in `qa_sections` so the template can render a table of contents.
  * Learning guides add comment markers to that QA part; a guide with any of them is returned as
    `guide_sections` (sections of learning units) for the template to lay out:
      <!-- stage: Foundations -->   groups the following `###` sections in the learning path
      <!-- unit: Title -->          starts a learning unit inside the current section
      <!-- goals -->, <!-- concept -->, <!-- example -->     the unit's introduction, before its questions
      <!-- challenge -->, <!-- solution -->, <!-- takeaways -->   after its questions
    `####` questions work as before; questions with no unit marker form an untitled unit.
"""

import csv
import html
import re
from dataclasses import dataclass, field
from pathlib import Path

from markdown_it import MarkdownIt

TITLE_IMAGE_MARKER = "<!-- TITLE_IMAGE -->"
QA_MARKER = "<!-- QA -->"
QA_NAV_SLOT = "<!-- qa-nav -->"  # where the template puts the contents list, between intro and questions
_QA_SPLIT_RE = re.compile(r'(<h([23]) id="([^"]+)">(.*?)</h\2>)', re.DOTALL)
PUBLISH_DATE_TOKEN = "{{PUBLISH_DATE}}"

_TITLE_RE = re.compile(r"^#{1,2}\s+(.+?)\s*$")
_IMAGE_RE = re.compile(r"^!\[(.*?)\]\((.*?)\)\s*$")
_FIGURE_RE = re.compile(r'<p><img src="([^"]*)" alt="([^"]*)" ([^>]*)/></p>')
_DATA_MARKER_RE = re.compile(r"<!--\s*(table|bars):\s*([\w.\-]+)\s*-->")
_UNIT_BLOCKS = ("goals", "concept", "example", "challenge", "solution", "takeaways")
_LEARN_MARKER_RE = re.compile(rf"^<!--\s*(stage|unit|{'|'.join(_UNIT_BLOCKS)})\s*(?::\s*(.*?))?\s*-->$")


@dataclass
class Question:
    id: str
    title: str  # inline HTML
    answer: str
    number: int


@dataclass
class Unit:
    id: str
    title: str
    questions: list[Question] = field(default_factory=list)
    goals: str = ""
    concept: str = ""
    example: str = ""
    challenge: str = ""
    solution: str = ""
    takeaways: str = ""

    @property
    def has_intro(self) -> bool:
        return bool(self.goals or self.concept or self.example)


@dataclass
class Section:
    id: str
    title: str
    stage: str = ""
    lead: str = ""
    units: list[Unit] = field(default_factory=list)

    @property
    def question_count(self) -> int:
        return sum(len(u.questions) for u in self.units)


def group_stages(sections: list[Section]) -> list[tuple[str, list[Section]]]:
    """Consecutive sections that share a stage, in document order."""
    stages: list[tuple[str, list[Section]]] = []
    for section in sections:
        if stages and stages[-1][0] == section.stage:
            stages[-1][1].append(section)
        else:
            stages.append((section.stage, [section]))
    return stages


@dataclass
class Rendered:
    title: str
    body_html: str
    cover: str | None = None
    cover_alt: str = ""
    summary: str = ""
    has_code: bool = False
    word_count: int = 0
    qa_sections: list[tuple[str, str, int]] = field(default_factory=list)  # (id, title, questions)
    guide_sections: list[Section] = field(default_factory=list)  # learning guides only

    @property
    def question_count(self) -> int:
        return sum(n for _, _, n in self.qa_sections)


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"[\s_]+", "-", text).strip("-")


def _render_image(self, tokens, idx, options, env):
    tokens[idx].attrSet("loading", "lazy")
    tokens[idx].attrSet("decoding", "async")
    return self.image(tokens, idx, options, env)


def _make_parser() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])
    md.add_render_rule("image", _render_image)
    return md


_md = _make_parser()


def _shift_headings(tokens) -> None:
    """Make the shallowest body heading an <h2> and give every heading an id for deep links."""
    levels = [int(t.tag[1]) for t in tokens if t.type == "heading_open"]
    if not levels:
        return
    shift = min(levels) - 2
    seen: dict[str, int] = {}
    for i, token in enumerate(tokens):
        if token.type not in ("heading_open", "heading_close"):
            continue
        level = max(2, min(6, int(token.tag[1]) - shift))
        token.tag = f"h{level}"
        if token.type == "heading_open":
            slug = slugify(tokens[i + 1].content) or "section"
            seen[slug] = seen.get(slug, 0) + 1
            token.attrSet("id", slug if seen[slug] == 1 else f"{slug}-{seen[slug]}")


def _post_process(body: str) -> str:
    body = _FIGURE_RE.sub(
        r'<figure><img src="\1" alt="\2" \3/><figcaption>\2</figcaption></figure>', body
    )
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    # Prism's line-numbers plugin reads the class from <pre>.
    return body.replace('<pre><code class="language-', '<pre class="line-numbers"><code class="language-')


def _extract_front(lines: list[str], extract_title: bool) -> tuple[str, str | None, str, list[str]]:
    """Pull title, cover image and publish-date line out of the markdown source."""
    title, cover, cover_alt = "", None, ""
    body: list[str] = []
    expecting_cover = False
    for line in lines:
        stripped = line.strip()
        if extract_title and not title and _TITLE_RE.match(stripped):
            title = _TITLE_RE.match(stripped).group(1)
            continue
        if PUBLISH_DATE_TOKEN in stripped and stripped.startswith("#"):
            continue
        if stripped == TITLE_IMAGE_MARKER:
            expecting_cover = True
            continue
        if expecting_cover and stripped:
            match = _IMAGE_RE.match(stripped)
            if match:
                cover_alt, cover = match.group(1).strip(), match.group(2).strip()
                expecting_cover = False
                continue
            expecting_cover = False
        body.append(line)
    return title, cover, cover_alt, body


def _first_paragraph_text(tokens, limit: int = 180) -> str:
    for i, token in enumerate(tokens):
        if token.type == "paragraph_open" and i + 1 < len(tokens):
            inline = tokens[i + 1]
            if inline.children and all(c.type == "image" for c in inline.children if c.type != "softbreak"):
                continue
            # Skip index-style paragraphs that are nothing but links.
            if len(re.sub(r"!?\[[^\]]*\]\([^)]*\)|\s", "", inline.content)) < 20:
                continue
            text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", inline.content)
            text = re.sub(r"[*_`<>]", "", text)
            text = " ".join(text.split())
            if len(text) < 40:
                continue
            if len(text) > limit:
                text = text[:limit].rsplit(" ", 1)[0] + "…"
            return text
    return ""


def _qa_cards(html_text: str) -> tuple[str, list[tuple[str, str, int]]]:
    """Turn the flat <h2> category / <h3> question / answer sequence into collapsible cards."""
    parts = _QA_SPLIT_RE.split(html_text)
    # split() yields: text, (full heading, level, id, inner), text, ...
    out = [parts[0]]
    sections: list[tuple[str, str, int]] = []
    open_card = False
    number = 0
    i = 1
    while i < len(parts):
        full, level, anchor, inner = parts[i:i + 4]
        following = parts[i + 4] if i + 4 < len(parts) else ""
        if open_card:
            out.append("</div></details>\n")
            open_card = False
        if level == "2":
            sections.append((anchor, re.sub(r"<[^>]+>", "", inner), 0))
            out.append(full)
        else:
            if sections:
                a, t, n = sections[-1]
                sections[-1] = (a, t, n + 1)
            number += 1
            out.append(f'<details class="qa" id="{anchor}"><summary data-n="{number}">{inner}</summary><div class="qa-answer">')
            open_card = True
        out.append(following)
        i += 5
    if open_card:
        out.append("</div></details>\n")
    return '<div class="qa-guide">' + "".join(out) + "</div>", sections


def _render_fragment(source: str) -> str:
    return _post_process(_md.render(source)).strip() if source.strip() else ""


def _is_learning_guide(lines: list[str]) -> bool:
    return any(_LEARN_MARKER_RE.match(line.strip()) for line in lines)


def _learning_sections(lines: list[str]) -> list[Section]:
    """Parse the QA part of a learning guide into sections, units and questions (see module docstring)."""
    sections: list[Section] = []
    seen: dict[str, int] = {}
    stage = ""
    target: tuple[object, str] | None = None  # (object, attribute) that collects the current lines
    buffer: list[str] = []
    in_fence = False
    number = 0

    def anchor(text: str) -> str:
        slug = slugify(text) or "section"
        seen[slug] = seen.get(slug, 0) + 1
        return slug if seen[slug] == 1 else f"{slug}-{seen[slug]}"

    def flush() -> None:
        text = "\n".join(buffer)
        buffer.clear()
        if target is None:
            if text.strip():
                raise ValueError(f"learning guide text outside a section, unit block or question: {text.strip()[:60]!r}")
            return
        obj, attr = target
        setattr(obj, attr, _render_fragment(text))

    def current_unit() -> Unit:
        if not sections:
            raise ValueError("learning guide marker or question before the first ### section")
        if not sections[-1].units:
            sections[-1].units.append(Unit(id="", title=""))
        return sections[-1].units[-1]

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
        marker = None if in_fence else _LEARN_MARKER_RE.match(stripped)
        heading = None if in_fence else re.match(r"^(#{3,4})\s+(.+?)\s*#*$", stripped)
        if not marker and not heading:
            buffer.append(line)
            continue
        flush()
        if heading and len(heading.group(1)) == 3:
            sections.append(Section(id=anchor(heading.group(2)), title=_md.renderInline(heading.group(2)).strip(),
                                    stage=stage))
            target = (sections[-1], "lead")
        elif heading:
            number += 1
            raw = heading.group(2)
            question = Question(id=anchor(raw), title=_md.renderInline(raw).strip(), answer="", number=number)
            current_unit().questions.append(question)
            target = (question, "answer")
        elif marker.group(1) == "stage":
            stage = marker.group(2) or ""
            target = None
        elif marker.group(1) == "unit":
            if not sections:
                raise ValueError("learning guide unit before the first ### section")
            title = marker.group(2) or ""
            sections[-1].units.append(Unit(id=anchor(title), title=_md.renderInline(title).strip()))
            target = None
        else:
            target = (current_unit(), marker.group(1))
    flush()
    return sections


def render_markdown(source: str, *, extract_title: bool = True, data_dir: Path | None = None) -> Rendered:
    """Render a post or project body. Projects keep their title in front matter (extract_title=False)."""
    title, cover, cover_alt, body_lines = _extract_front(source.splitlines(), extract_title)
    qa_at = next((i for i, line in enumerate(body_lines) if line.strip() == QA_MARKER), None)
    if qa_at is not None and _is_learning_guide(body_lines[qa_at + 1:]):
        tokens, intro_html = _render_body("\n".join(body_lines[:qa_at]), data_dir)
        sections = _learning_sections(body_lines[qa_at + 1:])
        fragments = [intro_html] + [
            html_part for s in sections for u in s.units
            for html_part in (u.goals, u.concept, u.example, u.challenge, u.solution, u.takeaways,
                              *(q.title + q.answer for q in u.questions))
        ]
        all_html = "\n".join(fragments)
        return Rendered(
            title=title, body_html=intro_html + "\n" + QA_NAV_SLOT + "\n", cover=cover, cover_alt=cover_alt,
            summary=_first_paragraph_text(tokens),
            has_code='class="language-' in all_html,
            word_count=len(re.sub(r"<[^>]+>", " ", all_html).split()),
            qa_sections=[(s.id, re.sub(r"<[^>]+>", "", s.title), s.question_count) for s in sections],
            guide_sections=sections,
        )
    if qa_at is not None:
        intro = _render_body("\n".join(body_lines[:qa_at]), data_dir)
        guide_tokens = _md.parse("\n".join(body_lines[qa_at + 1:]))
        _shift_headings(guide_tokens)
        guide_html, qa_sections = _qa_cards(_post_process(_md.renderer.render(guide_tokens, _md.options, {})))
        body_html = intro[1] + "\n" + QA_NAV_SLOT + "\n" + guide_html
        return Rendered(
            title=title, body_html=body_html, cover=cover, cover_alt=cover_alt,
            summary=_first_paragraph_text(intro[0]),
            has_code='class="language-' in body_html,
            word_count=len(re.sub(r"<[^>]+>", " ", body_html).split()),
            qa_sections=qa_sections,
        )
    tokens, body_html = _render_body("\n".join(body_lines), data_dir)
    return Rendered(
        title=title,
        body_html=body_html,
        cover=cover,
        cover_alt=cover_alt,
        summary=_first_paragraph_text(tokens),
        has_code='class="language-' in body_html,
        word_count=len(re.sub(r"<[^>]+>", " ", body_html).split()),
    )


def _render_body(body_source: str, data_dir: Path | None):
    """Markdown to (tokens, html) with the shared heading, figure and table conventions."""
    if data_dir is not None:
        body_source = _DATA_MARKER_RE.sub(lambda m: render_data_block(m.group(1), data_dir / m.group(2)), body_source)
    tokens = _md.parse(body_source)
    _shift_headings(tokens)
    return tokens, _post_process(_md.renderer.render(tokens, _md.options, {}))


def render_data_block(kind: str, csv_path: Path) -> str:
    """Render an exported CSV (e.g. a gold-table aggregate) as a table or bar chart.

    Returns an empty string when the file does not exist yet, so a project page can
    reference results before they are exported.
    """
    if not csv_path.exists():
        return ""
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if len(rows) < 2:
        return ""
    header, data = rows[0], rows[1:]
    esc = html.escape

    if kind == "table":
        head = "".join(f"<th>{esc(h)}</th>" for h in header)
        body = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>" for row in data)
        # _post_process adds the scroll wrapper, as for markdown tables.
        return f"\n<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>\n"

    # bars: first column is the label, second the numeric value.
    values = [float(row[1]) for row in data]
    peak = max(values) or 1
    items = "".join(
        f'<li><span class="bar-label">{esc(row[0])}</span>'
        f'<svg class="bar" viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true">'
        f'<rect width="{value / peak * 100:.2f}" height="10" rx="1"/></svg>'
        f'<span class="bar-value">{value:,.0f}</span></li>'
        for row, value in zip(data, values)
    )
    return f'\n<figure class="bar-chart"><figcaption>{esc(header[1])}</figcaption><ul>{items}</ul></figure>\n'

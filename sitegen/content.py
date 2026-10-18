"""Load blog posts, study guides and projects from content/ into plain objects the templates can use."""

import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from .config import POST_DIRS, POSTS_REGISTRY, PROJECTS_DIR
from .markdown import Section, group_stages, render_markdown

_FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WORDS_PER_MINUTE = 220


class ContentError(Exception):
    """Raised for content mistakes that would otherwise ship a broken page."""


@dataclass
class Post:
    slug: str
    lang: str
    title: str
    date: date
    body_html: str
    summary: str
    cover: str | None
    cover_alt: str
    has_code: bool
    reading_minutes: int
    languages: list[str]
    kind: str = "post"  # "post" (content/blog) or "guide" (content/guides), which live in their own sections
    qa_sections: list[tuple[str, str, int]] = field(default_factory=list)
    guide_sections: list[Section] = field(default_factory=list)  # learning guides: units with concepts and practice

    @property
    def question_count(self) -> int:
        return sum(n for _, _, n in self.qa_sections)

    @property
    def stages(self) -> list[tuple[str, list[Section]]]:
        return group_stages(self.guide_sections)


@dataclass
class Project:
    slug: str
    lang: str
    title: str
    summary: str
    updated: date
    started: str | None
    status: str
    stack: list[str]
    body_html: str
    cover: str | None = None
    cover_alt: str = ""
    repo: str | None = None
    demo: str | None = None
    has_code: bool = False
    reading_minutes: int = 1
    languages: list[str] = field(default_factory=list)
    insights: "Insights | None" = None
    featured: bool = False
    highlights: list[dict] = field(default_factory=list)  # [{value, label}] key figures for the home page
    points: list[str] = field(default_factory=list)       # one-line summaries shown under "What's inside"


@dataclass
class Insights:
    """A project's data page: narrative from content/projects/<lang>/insights/<slug>.md, charts
    drawn in the browser from the JSON the project's pipeline publishes at ``data_url``."""
    title: str
    summary: str
    body_html: str
    data_url: str


def _reading_minutes(word_count: int) -> int:
    return max(1, round(word_count / WORDS_PER_MINUTE))


def _absolute_image(path: str | None) -> str | None:
    """Covers are written relative to the post (../../images/x); the templates need /images/x."""
    if not path:
        return None
    return "/" + re.sub(r"^(\.\./)+", "", path).lstrip("/")


def load_registry(path: Path = POSTS_REGISTRY) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _find_post(lang: str, file_name: str, post_dirs: dict[str, Path]) -> tuple[str, Path] | None:
    """The kind of a registered post and its file, from the folder it sits in."""
    found = [(kind, d / lang / file_name) for kind, d in post_dirs.items() if (d / lang / file_name).exists()]
    if len(found) > 1:
        raise ContentError(f"{file_name} ({lang}) exists in more than one of: {', '.join(str(p) for _, p in found)}")
    return found[0] if found else None


def load_posts(lang: str, registry: list[dict] | None = None, post_dirs: dict[str, Path] = POST_DIRS) -> list[Post]:
    """Published blog posts and study guides for one language, newest first.

    A markdown file is only published once it has an entry in posts_metadata.json
    (see `python -m sitegen publish`); anything else under content/blog or content/guides is a draft.
    """
    registry = registry if registry is not None else load_registry()
    posts = []
    for entry in registry:
        lang_info = entry["languages"].get(lang)
        if not lang_info:
            continue
        found = _find_post(lang, lang_info["file_name"], post_dirs)
        if not found:
            raise ContentError(f"{entry['post_id']} is registered for '{lang}' but {lang_info['file_name']} is "
                               f"missing from {' and '.join(f'{d}/{lang}' for d in post_dirs.values())}")
        kind, md_path = found
        rendered = render_markdown(md_path.read_text(encoding="utf-8"))
        if (kind == "guide") != bool(rendered.qa_sections):
            raise ContentError(f"{md_path}: study guides (and only study guides) need a <!-- QA --> section; "
                               f"guides go in content/guides, articles in content/blog")
        posts.append(
            Post(
                slug=entry["post_id"],
                lang=lang,
                title=rendered.title or lang_info["title"],
                date=date.fromisoformat(entry["publication_date"]),
                body_html=rendered.body_html,
                summary=rendered.summary,
                cover=_absolute_image(rendered.cover or entry.get("title_image_url")),
                cover_alt=rendered.cover_alt,
                has_code=rendered.has_code,
                reading_minutes=_reading_minutes(rendered.word_count),
                languages=sorted(entry["languages"]),
                kind=kind,
                qa_sections=rendered.qa_sections,
                guide_sections=rendered.guide_sections,
            )
        )
    return sorted(posts, key=lambda p: p.date, reverse=True)


def find_drafts(registry: list[dict] | None = None, post_dirs: dict[str, Path] = POST_DIRS) -> list[Path]:
    registry = registry if registry is not None else load_registry()
    registered = {(lang, info["file_name"]) for e in registry for lang, info in e["languages"].items()}
    return sorted(p for d in post_dirs.values() for p in d.glob("*/*.md")
                  if (p.parent.name, p.name) not in registered)


def parse_front_matter(source: str) -> tuple[dict, str]:
    match = _FRONT_MATTER_RE.match(source)
    if not match:
        return {}, source
    return yaml.safe_load(match.group(1)) or {}, source[match.end():]


def load_projects(lang: str, projects_dir: Path = PROJECTS_DIR) -> list[Project]:
    """Projects for one language, most recently updated first."""
    projects = []
    for md_path in sorted((projects_dir / lang).glob("*.md")):
        meta, body = parse_front_matter(md_path.read_text(encoding="utf-8"))
        for required in ("title", "summary", "updated", "status"):
            if required not in meta:
                raise ContentError(f"{md_path}: front matter is missing '{required}'")
        slug = md_path.stem
        rendered = render_markdown(body, extract_title=False, data_dir=projects_dir / "data" / slug)
        insights = load_insights(projects_dir / lang / "insights" / f"{slug}.md")
        projects.append(
            Project(
                slug=slug,
                lang=lang,
                title=meta["title"],
                summary=meta["summary"],
                updated=meta["updated"] if isinstance(meta["updated"], date) else date.fromisoformat(meta["updated"]),
                started=str(meta["started"]) if meta.get("started") else None,
                status=meta["status"],
                stack=meta.get("stack", []),
                body_html=rendered.body_html,
                cover=_absolute_image(meta.get("cover")),
                cover_alt=meta.get("cover_alt", ""),
                repo=meta.get("repo"),
                demo=meta.get("demo"),
                has_code=rendered.has_code,
                reading_minutes=_reading_minutes(rendered.word_count),
                languages=sorted(p.parent.name for p in projects_dir.glob(f"*/{slug}.md")),
                insights=insights,
                featured=bool(meta.get("featured", False)),
                highlights=meta.get("highlights", []),
                points=meta.get("points", []),
            )
        )
    return sorted(projects, key=lambda p: p.updated, reverse=True)


def load_insights(md_path: Path) -> Insights | None:
    if not md_path.exists():
        return None
    meta, body = parse_front_matter(md_path.read_text(encoding="utf-8"))
    for required in ("title", "summary", "data_url"):
        if required not in meta:
            raise ContentError(f"{md_path}: front matter is missing '{required}'")
    rendered = render_markdown(body, extract_title=False)
    return Insights(title=meta["title"], summary=meta["summary"], body_html=rendered.body_html,
                    data_url=meta["data_url"])

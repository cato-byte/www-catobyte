"""Render the whole site into dist/.

URL layout (every link ends in .html because CloudFront serves S3 through its REST
endpoint, which does not resolve directory indexes):

    /index.html                     English home (canonical: /en/index.html)
    /{lang}/index.html              home
    /{lang}/{about,contact,legal}.html
    /{lang}/projects/index.html     /{lang}/projects/{slug}.html
    /{lang}/blog/index.html         /{lang}/blog/{slug}.html
    /pages/... and /post/...        redirects from the old site's URLs
"""

import hashlib
import json
import shutil
from dataclasses import dataclass, field
from datetime import date
from itertools import groupby
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup

from . import config
from .content import find_drafts, load_posts, load_projects, load_registry

LANGUAGE_NAMES = {"en": "English", "es": "Español", "fr": "Français"}
STATIC_PAGES = ["about", "contact", "legal"]

# Old page name -> new page key, so links shared before the redesign keep working.
LEGACY_PAGES = {
    "home": "home",
    "about": "about",
    "services": "about",
    "contact": "contact",
    "archive": "blog",
    "privacy_policy": "legal",
    "terms_of_service": "legal",
}

MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
           "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
           "août", "septembre", "octobre", "novembre", "décembre"],
}


def url_for(lang: str, page: str, slug: str | None = None) -> str:
    if page == "home":
        return f"/{lang}/index.html"
    if page in ("projects", "blog"):
        return f"/{lang}/{page}/index.html"
    if page == "project":
        return f"/{lang}/projects/{slug}.html"
    if page == "post":
        return f"/{lang}/blog/{slug}.html"
    return f"/{lang}/{page}.html"


def format_date(value: date, lang: str) -> str:
    month = MONTHS[lang][value.month - 1]
    if lang == "en":
        return f"{month} {value.day}, {value.year}"
    if lang == "es":
        return f"{value.day} de {month} de {value.year}"
    return f"{value.day} {month} {value.year}"


def format_month(value: str | date | None, lang: str) -> str:
    """'2026-09' or a date -> 'September 2026' / 'septiembre 2026'."""
    if not value:
        return ""
    year, month = str(value).split("-")[:2]
    return f"{MONTHS[lang][int(month) - 1]} {year}"


def asset_version() -> str:
    """Short hash of the CSS/JS so browsers fetch new files after a deploy (cache busting)."""
    digest = hashlib.sha256()
    for name in ("css/site.css", "css/prism.css", "js/site.js", "js/prism.js"):
        digest.update((config.ROOT / name).read_bytes())
    return digest.hexdigest()[:10]


@dataclass
class Page:
    kind: str
    url: str
    title: str
    description: str
    alternates: dict[str, str] = field(default_factory=dict)
    image: str | None = None
    has_code: bool = False
    noindex: bool = False


class Builder:
    def __init__(self, out_dir: Path = config.DIST_DIR, site: dict | None = None):
        self.out_dir = Path(out_dir)
        self.site = site or config.load_site()
        self.languages: list[str] = self.site["languages"]
        self.env = Environment(
            loader=FileSystemLoader(config.TEMPLATES_DIR),
            autoescape=select_autoescape(["html", "xml"]),
            undefined=StrictUndefined,  # a missing translation key fails the build instead of rendering blank
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["date"] = format_date
        self.env.filters["month"] = format_month
        self.env.globals.update(
            url_for=url_for, LANGUAGE_NAMES=LANGUAGE_NAMES, asset_version=asset_version(),
            cv=config.load_experience(),
        )
        self.sitemap: list[str] = []

    # ---- helpers -------------------------------------------------------------

    def load_i18n(self, lang: str) -> dict:
        with open(config.I18N_DIR / f"{lang}.json", encoding="utf-8") as f:
            return json.load(f)

    def write(self, url: str, text: str) -> None:
        path = self.out_dir / url.lstrip("/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def render(self, template: str, page: Page, lang: str, t: dict, **context) -> None:
        html = self.env.get_template(template).render(
            site=self.site, lang=lang, t=t, page=page, languages=self.languages,
            year=date.today().year, **context,
        )
        self.write(page.url, html)
        if not page.noindex:
            self.sitemap.append(page.url)

    def alternates(self, page: str, slug: str | None = None, available: list[str] | None = None) -> dict[str, str]:
        """Same page in the other languages; falls back to that language's section index."""
        fallback = {"post": "blog", "project": "projects"}.get(page, "home")
        return {
            lang: url_for(lang, page, slug) if available is None or lang in available else url_for(lang, fallback)
            for lang in self.languages
        }

    # ---- build steps ---------------------------------------------------------

    def build(self) -> None:
        if self.out_dir.exists():
            shutil.rmtree(self.out_dir)
        self.out_dir.mkdir(parents=True)
        self.copy_static()

        registry = load_registry()
        for lang in self.languages:
            self.build_language(lang, registry)

        self.build_root()
        self.build_redirects(registry)
        self.build_sitemap()

        for draft in find_drafts(registry):
            print(f"draft (not published): {draft.relative_to(config.ROOT)}")

    def copy_static(self) -> None:
        for name in config.STATIC_DIRS:
            src = config.ROOT / name
            if src.exists():
                shutil.copytree(src, self.out_dir / name)

    def build_language(self, lang: str, registry: list[dict]) -> None:
        t = self.load_i18n(lang)
        posts = load_posts(lang, registry)
        projects = load_projects(lang)

        self.render(
            "home.html",
            Page("home", url_for(lang, "home"), t["meta"]["site_title"], t["meta"]["description"],
                 self.alternates("home"), image="/images/og-default.png"),
            lang, t, projects=projects[:3], posts=posts[:3],
        )
        for name in STATIC_PAGES:
            self.render(
                f"{name}.html",
                Page(name, url_for(lang, name), t[name]["title"], t[name]["description"], self.alternates(name)),
                lang, t,
            )

        self.render(
            "projects.html",
            Page("projects", url_for(lang, "projects"), t["projects"]["title"], t["projects"]["description"],
                 self.alternates("projects")),
            lang, t, projects=projects,
        )
        for project in projects:
            self.render(
                "project.html",
                Page("project", url_for(lang, "project", project.slug), project.title, project.summary,
                     self.alternates("project", project.slug, project.languages),
                     image=project.cover, has_code=project.has_code),
                lang, t, project=project, body=Markup(project.body_html),
            )

        posts_by_year = [(year, list(group)) for year, group in groupby(posts, key=lambda p: p.date.year)]
        self.render(
            "blog.html",
            Page("blog", url_for(lang, "blog"), t["blog"]["title"], t["blog"]["description"], self.alternates("blog")),
            lang, t, posts_by_year=posts_by_year,
        )
        for i, post in enumerate(posts):
            others = [p for p in posts if p.slug != post.slug][:3]
            self.render(
                "post.html",
                Page("post", url_for(lang, "post", post.slug), post.title, post.summary or post.title,
                     self.alternates("post", post.slug, post.languages), image=post.cover, has_code=post.has_code),
                lang, t, post=post, body=Markup(post.body_html), others=others,
            )

        self.render(
            "404.html",
            Page("404", f"/{lang}/404.html", t["not_found"]["title"], t["not_found"]["title"],
                 self.alternates("home"), noindex=True),
            lang, t,
        )

    def build_root(self) -> None:
        """The domain root serves the default-language home, plus a root 404 for CloudFront."""
        lang = self.site["default_language"]
        shutil.copy(self.out_dir / lang / "index.html", self.out_dir / "index.html")
        shutil.copy(self.out_dir / lang / "404.html", self.out_dir / "404.html")
        self.write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {self.site['base_url']}/sitemap.xml\n")

    def build_redirects(self, registry: list[dict]) -> None:
        template = self.env.get_template("redirect.html")
        for lang in self.languages:
            for old, new in LEGACY_PAGES.items():
                self.write(f"/pages/{lang}/{old}.html", template.render(target=url_for(lang, new)))
            for entry in registry:
                if lang in entry["languages"]:
                    target = url_for(lang, "post", entry["post_id"])
                    self.write(f"/post/{lang}/{entry['post_id']}.html", template.render(target=target))

    def build_sitemap(self) -> None:
        base = self.site["base_url"]
        urls = "".join(f"  <url><loc>{base}{url}</loc></url>\n" for url in sorted(set(self.sitemap)))
        self.write(
            "/sitemap.xml",
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
        )

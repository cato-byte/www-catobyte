"""Checks on the fully built site: the things that would break silently in production."""

import json
import posixpath
from pathlib import Path
import re
from urllib.parse import unquote, urlparse

import pytest

from sitegen import config
from sitegen.content import load_projects, load_registry

LANGS = config.load_site()["languages"]


def _flatten_keys(data, prefix=""):
    if isinstance(data, dict):
        keys = set()
        for key, value in data.items():
            keys |= _flatten_keys(value, f"{prefix}.{key}" if prefix else key)
        return keys
    if isinstance(data, list):
        keys = set()
        for i, value in enumerate(data):
            keys |= _flatten_keys(value, f"{prefix}[{i}]")
        return keys
    return {prefix}


def test_translations_have_identical_keys():
    key_sets = {lang: _flatten_keys(json.loads((config.I18N_DIR / f"{lang}.json").read_text("utf-8"))) for lang in LANGS}
    reference = key_sets[LANGS[0]]
    for lang, keys in key_sets.items():
        assert keys == reference, f"{lang}.json: missing {reference - keys}, extra {keys - reference}"


@pytest.mark.parametrize("lang", LANGS)
def test_expected_pages_exist(dist, lang):
    expected = ["index.html", "about.html", "contact.html", "legal.html", "404.html",
                "projects/index.html", "blog/index.html"]
    expected += [f"blog/{e['post_id']}.html" for e in load_registry() if lang in e["languages"]]
    expected += [f"projects/{p.slug}.html" for p in load_projects(lang)]
    missing = [p for p in expected if not (dist / lang / p).exists()]
    assert not missing


def test_root_files_exist(dist):
    for name in ("index.html", "404.html", "robots.txt", "sitemap.xml"):
        assert (dist / name).exists(), name


def test_every_page_has_required_head_and_structure(pages):
    problems = []
    for rel, soup in pages.items():
        html = soup.find("html")
        if not html or not html.get("lang"):
            problems.append(f"{rel}: <html lang> missing")
        if not (soup.title and soup.title.get_text(strip=True)):
            problems.append(f"{rel}: empty <title>")
        if not soup.find("meta", attrs={"name": "viewport"}):
            problems.append(f"{rel}: no viewport meta (breaks mobile)")
        description = soup.find("meta", attrs={"name": "description"})
        if not description or not description.get("content", "").strip():
            problems.append(f"{rel}: empty meta description")
        if not soup.find("link", rel="canonical"):
            problems.append(f"{rel}: no canonical link")
        if len(soup.find_all("h1")) != 1:
            problems.append(f"{rel}: {len(soup.find_all('h1'))} <h1> elements")
        if len(soup.find_all("main")) != 1:
            problems.append(f"{rel}: {len(soup.find_all('main'))} <main> elements")
    assert not problems, "\n".join(problems)


def test_page_language_matches_its_folder(pages):
    for rel, soup in pages.items():
        if rel.parts[0] in LANGS:
            assert soup.find("html")["lang"] == rel.parts[0], rel


def test_doctype_present(dist):
    for path in dist.rglob("*.html"):
        assert path.read_text(encoding="utf-8").lstrip().lower().startswith("<!doctype html>"), path


def _resolve(page_rel, url):
    """Map an internal URL from a page to a path relative to dist/, or None if external."""
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc or url.startswith(("mailto:", "tel:", "data:", "#")):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    if path.startswith("/"):
        return path.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(page_rel.as_posix()), path))


def test_no_broken_internal_links_or_images(dist, pages):
    broken = []
    for rel, soup in pages.items():
        for tag, attr in (("a", "href"), ("img", "src"), ("link", "href"), ("script", "src")):
            for el in soup.find_all(tag):
                url = el.get(attr)
                if not url:
                    continue
                target = _resolve(rel, url)
                if target is not None and not (dist / target).is_file():
                    broken.append(f"{rel}: {tag} {url}")
    assert not broken, "\n".join(sorted(set(broken)))


def test_in_page_anchors_exist(pages):
    broken = []
    for rel, soup in pages.items():
        targets = {el.get("id") for el in soup.find_all(id=True)} | {el.get("name") for el in soup.find_all("a", attrs={"name": True})}
        for a in soup.find_all("a", href=re.compile(r"^#.")):
            if unquote(a["href"][1:]) not in targets:
                broken.append(f"{rel}: {a['href']}")
    assert not broken, "\n".join(broken)


def test_images_have_alt_attribute(pages):
    missing = [f"{rel}: {img.get('src')}" for rel, soup in pages.items() for img in soup.find_all("img") if img.get("alt") is None]
    assert not missing, "\n".join(missing)


def test_no_unrendered_template_syntax(pages):
    leaks = []
    for rel, soup in pages.items():
        for code in soup.find_all(["code", "pre", "script"]):
            code.decompose()
        text = str(soup)
        if re.search(r"\{\{|\{%|PUBLISH_DATE|<!-- (table|bars):", text):
            leaks.append(str(rel))
    assert not leaks, leaks


def test_hreflang_alternates_point_to_real_pages(dist, pages, site):
    broken = []
    for rel, soup in pages.items():
        for link in soup.find_all("link", rel="alternate", hreflang=True):
            path = link["href"].removeprefix(site["base_url"]).lstrip("/")
            if not (dist / path).is_file():
                broken.append(f"{rel}: {link['hreflang']} -> {link['href']}")
    assert not broken, "\n".join(broken)


def test_legacy_urls_redirect_to_existing_pages(dist):
    stubs = list((dist / "pages").rglob("*.html")) + list((dist / "post").rglob("*.html"))
    assert stubs
    for stub in stubs:
        target = re.search(r'url=([^"]+)"', stub.read_text(encoding="utf-8")).group(1)
        assert (dist / target.lstrip("/")).is_file(), f"{stub} -> {target}"


def test_sitemap_lists_only_existing_pages(dist, site):
    locs = re.findall(r"<loc>(.*?)</loc>", (dist / "sitemap.xml").read_text(encoding="utf-8"))
    assert locs
    for loc in locs:
        assert (dist / loc.removeprefix(site["base_url"]).lstrip("/")).is_file(), loc
    assert not any("404" in loc for loc in locs)


def test_structured_data_is_valid_json(pages):
    for rel, soup in pages.items():
        for script in soup.find_all("script", type="application/ld+json"):
            json.loads(script.string)


def test_homepage_shows_latest_project(pages):
    for lang in LANGS:
        latest = load_projects(lang)[0]
        home = pages[Path(lang) / "index.html"]
        assert home.find("a", href=f"/{lang}/projects/{latest.slug}.html"), lang


def test_nav_has_projects_link_everywhere(pages):
    for rel, soup in pages.items():
        nav = soup.find("nav", id="site-nav")
        assert nav and nav.find("a", href=re.compile(r"/projects/index\.html$")), rel


def test_experience_is_translated_in_every_language():
    cv = config.load_experience()
    for job in cv["experience"]:
        for lang in LANGS:
            assert job[lang]["role"], f"{job['company']}: no role in {lang}"
        for mission in job.get("missions", []):
            assert all(mission.get(lang) for lang in LANGS), mission["client"]
    for entry in cv["education"] + cv["spoken_languages"]:
        assert all(entry.get(lang) for lang in LANGS), entry


def test_about_page_lists_every_employer(pages):
    companies = [job["company"] for job in config.load_experience()["experience"]]
    for lang in LANGS:
        text = pages[Path(lang) / "about.html"].get_text()
        assert all(company in text for company in companies), lang


def _projects_with_insights(lang):
    return [p for p in load_projects(lang) if p.insights]


@pytest.mark.parametrize("lang", LANGS)
def test_insights_pages_exist_and_are_linked_from_their_project(dist, pages, lang):
    projects = _projects_with_insights(lang)
    assert projects, "the registry project should have an insights page"
    for project in projects:
        url = f"/{lang}/projects/{project.slug}/insights.html"
        page = pages[Path(url.lstrip("/"))]
        root = page.find(attrs={"data-insights": True})
        assert root and root["data-src"].startswith("/") and root["data-src"].endswith("/data/")
        # Chart labels for the script. Read from disk: another test strips <script> from the shared soups.
        raw = (dist / url.lstrip("/")).read_text("utf-8")
        json.loads(re.search(r'<script type="application/json" id="insights-i18n">(.*?)</script>', raw, re.S).group(1))
        assert page.find(attrs={"data-viz": "map"})
        assert pages[Path(lang) / "projects" / f"{project.slug}.html"].find("a", href=url), lang


def test_insights_pages_use_only_known_charts(pages):
    known = set(re.findall(r"^  VIZ\.(\w+) =", (config.ROOT / "js" / "insights.js").read_text("utf-8"), re.M))
    for rel, soup in pages.items():
        for node in soup.find_all(attrs={"data-viz": True}):
            assert node["data-viz"] in known, f"{rel}: unknown chart {node['data-viz']}"


def test_insights_page_stats_and_reasons_exist_in_every_language():
    script = (config.ROOT / "js" / "insights.js").read_text("utf-8")
    for lang in LANGS:
        for project in _projects_with_insights(lang):
            for stat in re.findall(r'data-stat="(\w+)"', project.insights.body_html):
                assert re.search(rf"\b{stat}:", script), f"{lang}: data-stat {stat} is never computed"


def test_home_features_the_flagship_project(pages):
    for lang in LANGS:
        featured = next(p for p in load_projects(lang) if p.featured)
        home = pages[Path(lang) / "index.html"]
        section = home.find("section", attrs={"aria-labelledby": "featured-title"})
        assert section and section.find("a", href=f"/{lang}/projects/{featured.slug}/insights.html"), lang


def test_deploy_never_uploads_pipeline_data():
    script = (config.ROOT / "scripts" / "deploy.sh").read_text("utf-8")
    assert '--exclude "*/projects/*/data/*"' in script


@pytest.mark.parametrize("lang", LANGS)
def test_study_guides_render_question_cards(pages, lang):
    for entry in load_registry():
        if lang not in entry["languages"] or not entry["post_id"].endswith("study_guide"):
            continue
        soup = pages[Path(lang) / "blog" / f"{entry['post_id']}.html"]
        cards = soup.select("details.qa")
        if entry["post_id"] == "pyspark_study_guide":
            continue  # written before the question-card format
        assert len(cards) >= 100, f"{entry['post_id']} ({lang}): {len(cards)} questions"
        assert soup.find("nav", class_="qa-toc")


def test_image_archive_is_not_published(dist):
    assert (dist / "images").is_dir()
    assert not (dist / "images" / "archive").exists()

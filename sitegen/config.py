"""Paths and site settings shared by every build step."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

CONTENT_DIR = ROOT / "content"
BLOG_DIR = CONTENT_DIR / "blog"
GUIDES_DIR = CONTENT_DIR / "guides"
# Where each kind of post lives: content/<folder>/<lang>/<post_id>.md. Both share one registry.
POST_DIRS = {"post": BLOG_DIR, "guide": GUIDES_DIR}
PROJECTS_DIR = CONTENT_DIR / "projects"
POSTS_REGISTRY = ROOT / "metadata" / "posts_metadata.json"
EXPERIENCE_FILE = CONTENT_DIR / "experience.yaml"

TEMPLATES_DIR = ROOT / "templates"
I18N_DIR = TEMPLATES_DIR / "i18n"

# Copied verbatim into the output. Missing folders (e.g. files/ before a CV exists) are skipped.
STATIC_DIRS = ["css", "js", "images", "files"]

DIST_DIR = ROOT / "dist"
# Pipeline output fetched for a local preview (scripts/fetch_project_data.sh); never committed.
LOCAL_DATA_DIR = ROOT / "local_data"
SITE_FILE = ROOT / "site.yaml"


def load_site(path: Path = SITE_FILE) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_experience(path: Path = EXPERIENCE_FILE) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

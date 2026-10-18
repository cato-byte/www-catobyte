from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from sitegen import config
from sitegen.build import Builder


@pytest.fixture(scope="session")
def site() -> dict:
    return config.load_site()


@pytest.fixture(scope="session")
def dist(tmp_path_factory, site) -> Path:
    """Build the real site once into a temp dir; every integration test reads from it."""
    out = tmp_path_factory.mktemp("dist")
    Builder(out_dir=out, site=site).build()
    return out


@pytest.fixture(scope="session")
def pages(dist) -> dict[Path, BeautifulSoup]:
    """Every generated HTML page except the redirect stubs, parsed once."""
    parsed = {}
    for path in sorted(dist.rglob("*.html")):
        rel = path.relative_to(dist)
        text = path.read_text(encoding="utf-8")
        if rel.parts[0] in ("pages", "post") or 'http-equiv="refresh"' in text:
            continue
        parsed[rel] = BeautifulSoup(text, "html.parser")
    return parsed

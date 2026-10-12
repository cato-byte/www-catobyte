"""Command line entry point.

    python -m sitegen build              render the site into dist/
    python -m sitegen serve [--port N]   build, then serve dist/ on http://localhost:N
    python -m sitegen publish <post_id>  add a draft post to the registry with today's date
    python -m sitegen drafts             list markdown files that are not published yet
"""

import argparse
import functools
import http.server
import json
from datetime import date

from . import config
from .build import Builder
from .content import find_drafts, load_registry
from .markdown import render_markdown


def publish(post_id: str) -> None:
    registry = load_registry()
    if any(entry["post_id"] == post_id for entry in registry):
        raise SystemExit(f"{post_id} is already published")

    languages = {}
    for md_path in sorted(config.BLOG_DIR.glob(f"*/{post_id}.md")):
        rendered = render_markdown(md_path.read_text(encoding="utf-8"))
        languages[md_path.parent.name] = {"file_name": md_path.name, "title": rendered.title}
    if not languages:
        raise SystemExit(f"No content/blog/<lang>/{post_id}.md found")

    today = date.today().isoformat()
    registry.append({"post_id": post_id, "languages": languages, "creation_date": today, "publication_date": today})
    with open(config.POSTS_REGISTRY, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4, ensure_ascii=False)
    print(f"Published {post_id} ({', '.join(languages)}) on {today}")


def serve(port: int) -> None:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(config.DIST_DIR))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Serving dist/ on http://localhost:{port}/en/index.html (Ctrl+C to stop)")
        httpd.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(prog="sitegen")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    serve_parser = sub.add_parser("serve")
    serve_parser.add_argument("--port", type=int, default=8000)
    publish_parser = sub.add_parser("publish")
    publish_parser.add_argument("post_id")
    sub.add_parser("drafts")
    args = parser.parse_args()

    if args.command == "build":
        Builder().build()
        print(f"Site built in {config.DIST_DIR}")
    elif args.command == "serve":
        Builder().build()
        serve(args.port)
    elif args.command == "publish":
        publish(args.post_id)
    elif args.command == "drafts":
        for path in find_drafts():
            print(path.relative_to(config.ROOT))


if __name__ == "__main__":
    main()

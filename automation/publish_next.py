"""Publish one randomly selected, previously unpublished SEO article.

Designed for GitHub Actions, but can also be run locally:
    python automation/publish_next.py

The script:
1. Loads the prewritten article queue.
2. Excludes slugs already recorded as published.
3. Securely selects one remaining article at random.
4. Renders the article using the shared site template.
5. Records the slug to prevent future duplicates.
6. Rebuilds the Resource Center and sitemap.
"""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import secrets
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_DIR = ROOT / "automation"
sys.path.insert(0, str(AUTOMATION_DIR))

from article_template import render_article, rebuild_resources_index, rebuild_sitemap

QUEUE_PATH = AUTOMATION_DIR / "article_queue.json"
PUBLISHED_PATH = AUTOMATION_DIR / "published_queue.json"


def load_json_list(path: Path) -> list[Any]:
    """Read and validate a JSON array."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Required file is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, list):
        raise SystemExit(f"Expected a JSON array in {path}")
    return data


def validate_queue(queue: list[Any]) -> list[dict[str, Any]]:
    """Validate required article fields and reject duplicate slugs."""
    required = {"slug", "title", "category", "description", "sections"}
    validated: list[dict[str, Any]] = []
    seen_slugs: set[str] = set()

    for index, item in enumerate(queue, start=1):
        if not isinstance(item, dict):
            raise SystemExit(f"Queue item {index} is not an object")

        missing = required.difference(item)
        if missing:
            raise SystemExit(
                f"Queue item {index} is missing required fields: "
                + ", ".join(sorted(missing))
            )

        slug = str(item["slug"]).strip()
        if not slug:
            raise SystemExit(f"Queue item {index} has an empty slug")
        if slug in seen_slugs:
            raise SystemExit(f"Duplicate article slug in queue: {slug}")

        seen_slugs.add(slug)
        validated.append(item)

    return validated


def main() -> int:
    queue = validate_queue(load_json_list(QUEUE_PATH))
    published_raw = load_json_list(PUBLISHED_PATH)
    published = [str(slug) for slug in published_raw]
    published_set = set(published)

    remaining = [post for post in queue if str(post["slug"]) not in published_set]
    if not remaining:
        print("No unpublished queued articles remain. Add more entries to article_queue.json.")
        return 0

    # SystemRandom uses the operating system's randomness source and avoids
    # predictable selections caused by a fixed pseudorandom seed.
    post = secrets.SystemRandom().choice(remaining)
    slug = str(post["slug"])

    output_dir = ROOT / "resources" / slug
    output_file = output_dir / "index.html"

    # A pre-existing page that is not tracked as published could indicate a
    # partial/manual publication. Stop rather than silently overwrite it.
    if output_file.exists():
        raise SystemExit(
            f"Refusing to overwrite existing article not recorded as published: {output_file}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        render_article(post, date.today().isoformat()),
        encoding="utf-8",
    )

    published.append(slug)
    PUBLISHED_PATH.write_text(
        json.dumps(published, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    rebuild_resources_index(ROOT)
    rebuild_sitemap(ROOT)

    print(f"Published random article: {post['title']}")
    print(f"Remaining unpublished articles: {len(remaining) - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

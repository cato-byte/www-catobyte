"""Generate the 1024x1024 covers of the study guides and articles, in the site's dark style.

Run from the repo root:  python scripts/make_guide_covers.py
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path("/usr/share/fonts/truetype/noto")
SIZE = 1024

NAVY = (11, 17, 32)
TEXT = (230, 235, 245)
MUTED = (154, 168, 191)
ACCENT = (126, 162, 255)
WHITE = (255, 255, 255)

# file stem: (tile text, tile colour, title, subtitle, footer)
GUIDE = "~200 questions · catobyte.co"
ARTICLE = "Article · catobyte.co"
COVERS = {
    "pyspark_study_guide": ("PS", (226, 90, 27), "PySpark", "DataFrames, Spark SQL, joins, shuffles and performance tuning", GUIDE),
    "python_study_guide": ("Py", (55, 118, 171), "Python", "The language, the standard library and Python for data engineering", "~220 questions · catobyte.co"),
    "postgres_study_guide": ("PG", (51, 103, 145), "PostgreSQL", "SQL, indexes, transactions and MVCC, performance and administration", GUIDE),
    "databricks_study_guide": ("DB", (255, 54, 33), "Databricks", "Lakehouse, Delta Lake, Lakeflow pipelines, Unity Catalog and performance", "~250 questions · catobyte.co"),
    "airflow_study_guide": ("AF", (1, 124, 238), "Apache Airflow", "DAGs, operators, scheduling, sensors and deployment", GUIDE),
    "snowflake_study_guide": ("SF", (41, 181, 232), "Snowflake", "Warehouses, storage, loading, security and cost", "~225 questions · catobyte.co"),
    "aws_glue_study_guide": ("Glue", (140, 79, 255), "AWS Glue", "Data Catalog, crawlers, Spark ETL jobs and workflows", GUIDE),
    "aws_athena_study_guide": ("Ath", (110, 60, 220), "Amazon Athena", "Serverless SQL on S3, partitions, formats and cost", GUIDE),
    "aws_rds_study_guide": ("RDS", (201, 37, 209), "Amazon RDS", "Engines, Multi-AZ, replicas, backups and Aurora", GUIDE),
    "hadoop_study_guide": ("Hd", (196, 148, 10), "Hadoop", "HDFS, YARN, MapReduce, Hive and the ecosystem", GUIDE),
    "data_warehousing_study_guide": ("DW", (15, 138, 95), "Data Warehousing", "Dimensional modeling, SCDs, loading and query performance", GUIDE),
    "data_architecture_study_guide": ("DA", (37, 84, 217), "Data Architecture", "Kimball, Inmon, Data Vault, lakehouse, mesh and streaming", GUIDE),
    "scala_study_guide": ("Sc", (220, 50, 47), "Scala", "Types, collections, functional programming, concurrency and Spark", "~220 questions · catobyte.co"),
    "cicd_data_study_guide": ("CI", (36, 41, 47), "CI/CD for Data", "Git, testing, GitHub Actions, environments and deployment", GUIDE),
    "data_architecture_patterns": ("Arch", (37, 84, 217), "Data architecture", "Kimball, microservices, medallion and how to choose", ARTICLE),
    "testing_and_performance_big_data": ("Test", (15, 138, 95), "Big data testing", "Proving pipelines right, then making them fast", ARTICLE),
    "cicd_automation_for_data": ("CI/CD", (36, 41, 47), "Data CI/CD", "Automating data pipelines, with GitHub Actions examples", ARTICLE),
    "prompt_engineering_in_practice": ("Prompt", (217, 119, 87), "Prompt engineering", "Techniques that still matter, with examples", ARTICLE),
    "retrieval_augmented_generation_in_practice": ("RAG", (16, 163, 127), "RAG in practice", "Retrieval, reranking, grounded answers and evaluation", ARTICLE),
    "ai_agents_how_to_use_them": ("Agents", (124, 58, 237), "AI agents", "How they work and how to use Claude, Codex and others", ARTICLE),
    "ai_agents_and_data_engineering": ("AI", (124, 58, 237), "AI agents and data", "What teams delegate, the risks and what changes for the role", ARTICLE),
}


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / f"NotoSans-{weight}.ttf"), size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if draw.textlength(candidate, font=fnt) <= width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    return lines + [line]


def cover(path: Path, tile: str, colour, title: str, subtitle: str, footer: str) -> None:
    img = Image.new("RGB", (SIZE, SIZE), NAVY)
    d = ImageDraw.Draw(img)
    box = (96, 120, 396, 420)
    d.rounded_rectangle(box, radius=48, fill=colour)
    size = 120
    while d.textlength(tile, font=font("Bold", size)) > 240:
        size -= 4
    d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), tile, font=font("Bold", size), fill=WHITE, anchor="mm")

    y = 490
    title_font = font("Bold", 76)
    for line in wrap(d, title, title_font, 830):
        d.text((96, y), line, font=title_font, fill=TEXT)
        y += 92
    y += 24
    sub_font = font("Regular", 36)
    for line in wrap(d, subtitle, sub_font, 620):
        d.text((96, y), line, font=sub_font, fill=MUTED)
        y += 56

    d.text((96, 900), footer, font=font("SemiBold", 32), fill=ACCENT)
    d.rectangle((0, SIZE - 16, SIZE, SIZE), fill=ACCENT)
    img.save(path, optimize=True)


if __name__ == "__main__":
    # Existing files are kept. --force redraws the study guide covers; --force <stem> ... redraws only
    # the named covers. Article placeholders are only redrawn by name, since most have been replaced
    # by illustrations made in an external tool.
    force = "--force" in sys.argv
    only = {arg for arg in sys.argv[1:] if not arg.startswith("--")}
    for stem, spec in COVERS.items():
        if only and stem not in only:
            continue
        if force and not only and spec[-1] == ARTICLE:
            continue
        path = ROOT / "images" / f"{stem}_title_img.png"
        if force or not path.exists():
            cover(path, *spec)
            print(path.relative_to(ROOT))

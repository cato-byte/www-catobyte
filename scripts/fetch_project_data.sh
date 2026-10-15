#!/bin/bash
# Download the data a project's insights page reads, for a local preview.
#
#   ./scripts/fetch_project_data.sh                       # eu-company-registry, from the live site
#   BUCKET=<bucket> ./scripts/fetch_project_data.sh       # same files straight from S3
#
# The pipeline publishes these files itself (its last task writes them into the website bucket,
# under /en/projects/<slug>/data/), so they are never committed here and deploy.sh never uploads
# them: a site deploy must not overwrite a newer pipeline run with an old local copy.
# The build copies local_data/<slug>/ into dist/ so `python -m sitegen serve` shows real data.
set -euo pipefail

SLUG="${1:-eu-company-registry}"
BASE_URL="${BASE_URL:-https://www.catobyte.co}"
FILES="meta.json pipeline.json insights.json industry_by_country.json cities.geojson fishing.geojson"

cd "$(dirname "$0")/.."
OUT="local_data/$SLUG"
mkdir -p "$OUT"

if [ -n "${BUCKET:-}" ]; then
  aws s3 sync "s3://$BUCKET/en/projects/$SLUG/data/" "$OUT/" --no-progress
else
  for name in $FILES; do
    curl -sSfL --compressed "$BASE_URL/en/projects/$SLUG/data/$name" -o "$OUT/$name"
  done
fi
echo "Data for $SLUG in $OUT:"
ls -l "$OUT"

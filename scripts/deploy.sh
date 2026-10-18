#!/bin/bash
# Test, build and upload the site to S3, then invalidate CloudFront.
#
#   BUCKET=<bucket> DISTRIBUTION_ID=<id> ./scripts/deploy.sh
#   DRY_RUN=1 BUCKET=<bucket> ./scripts/deploy.sh      # show what would change, upload nothing
#
# DISTRIBUTION_ID is optional: without it the files are uploaded and CloudFront serves
# them once its cache expires. Used locally and by .github/workflows/ci.yml.
#
# Files are only added or overwritten, never deleted, so a mistake can't wipe the bucket. A page the
# build no longer produces (a moved or unpublished post) has to be removed from the bucket by hand.
# Old URLs (/pages/..., /post/...) are overwritten by redirect pages from the build.
# Project data under */projects/*/data/ is excluded: the pipeline publishes it there itself,
# and a local preview copy (local_data/) must never overwrite a newer pipeline run.
set -euo pipefail

: "${BUCKET:?Set BUCKET to the S3 bucket name}"
PYTHON="${PYTHON:-./kunturvenv/bin/python}"
DRY=${DRY_RUN:+--dryrun}

cd "$(dirname "$0")/.."

"$PYTHON" -m pytest -q
"$PYTHON" -m sitegen build

# Assets (css, js, images) can be cached for a day: their URLs carry a content hash (?v=...).
# HTML, the sitemap and robots.txt for 5 minutes, so content edits show up quickly.
aws s3 sync dist "s3://$BUCKET" $DRY --no-progress \
  --exclude "*/projects/*/data/*" \
  --exclude "*.html" --exclude "*.xml" --exclude "*.txt" \
  --cache-control "public, max-age=86400"
aws s3 sync dist "s3://$BUCKET" $DRY --no-progress \
  --exclude "*" --include "*.html" --include "*.xml" --include "*.txt" \
  --cache-control "public, max-age=300"

if [ -n "${DRY_RUN:-}" ]; then
  echo "Dry run only: nothing uploaded."
elif [ -n "${DISTRIBUTION_ID:-}" ]; then
  aws cloudfront create-invalidation --distribution-id "$DISTRIBUTION_ID" --paths "/*" \
    --query 'Invalidation.Id' --output text
  echo "Deployed to s3://$BUCKET and invalidated CloudFront."
else
  echo "Deployed to s3://$BUCKET. No DISTRIBUTION_ID set: CloudFront will serve the new files once its cache expires."
fi

#!/bin/bash
# Create the virtual environment and install build + test dependencies.
set -euo pipefail
python3 -m venv kunturvenv
./kunturvenv/bin/pip install --upgrade pip
./kunturvenv/bin/pip install -r requirements-dev.txt

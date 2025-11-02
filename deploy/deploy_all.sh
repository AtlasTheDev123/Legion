#!/usr/bin/env bash
set -euo pipefail
python -c "import json,sys; json.load(open('schemas/functions.json'))" || { echo "functions.json invalid"; exit 1; }
zip -r nexus_legion_x_omega_package.zip .

#!/usr/bin/env bash

# On GitHub Action, use "xml", "term" otherwise.
report=$([ ! -z "$GITHUB_ACTION" ] && echo "xml" || echo "term")

pytest tests --doctest-modules mlflow_extend --cov mlflow_extend --cov-report="$report" \
  --verbose --showlocals --color=yes --durations=30 --basetemp .pytest_basetemp "$@"

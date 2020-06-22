#!/usr/bin/env bash

# On GitHub Action, use "xml" otherwise "term" .
cov_report_type=$([ ! -z "$GITHUB_ACTION" ] && echo "xml" || echo "term")

pytest tests \
  --doctest-modules mlflow_extend \
  --cov mlflow_extend \
  --cov-report="$cov_report_type" \
  --verbose \
  --showlocals \
  --color=yes \
  --durations=30 \
  --basetemp .pytest_basetemp \
  "$@"

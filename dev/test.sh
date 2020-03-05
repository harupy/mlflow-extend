#!/usr/bin/env bash

pytest tests --doctest-modules mlflow_extend --cov mlflow_extend --cov-report=xml \
  --verbose --showlocals --color=yes --durations=30 --basetemp .pytest_basetemp "$@"



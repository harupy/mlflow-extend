#!/usr/bin/env bash

pytest . \
  --cov mlflow_extend --cov-report html --verbose --showlocals \
  --basetemp .pytest_basetemp --color=yes --durations=30 --doctest-modules mlflow_extend "$@"

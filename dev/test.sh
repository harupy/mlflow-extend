#!/usr/bin/env bash

pytest --cov mlflow_extend --verbose --showlocals --color=yes --durations=30 --doctest-modules mlflow_extend .

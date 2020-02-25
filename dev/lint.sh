#!/usr/bin/env bash

exit_code=0

black --check tests mlflow_extend
[[ $? = 1 ]] && exit_code=1

flake8 tests mlflow_extend
[[ $? = 1 ]] && exit_code=1

exit $exit_code

#!/usr/bin/env bash

exit_code=0

python_ver=$(python -c 'import sys; print("{}.{}".format(*sys.version_info[:2]))')

# Black does not support python 3.5.
if [ ! "$python_ver" == "3.5" ]; then
  black --check tests mlflow_extend
  [[ $? = 1 ]] && exit_code=1
fi

flake8 tests mlflow_extend
[[ $? = 1 ]] && exit_code=1

exit $exit_code

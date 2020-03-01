#!/usr/bin/env bash

exit_code=0

python_ver=$(python -c 'import sys; print("{}.{}".format(*sys.version_info[:2]))')

# Black does not support python 3.5.
if [ ! "$python_ver" == "3.5" ]; then
  black --check .
  exit_code=$(( $? | $exit_code ))
fi

isort --check-only .
exit_code=$(( $? | $exit_code ))

flake8 .
exit_code=$(( $? | $exit_code ))

exit $exit_code

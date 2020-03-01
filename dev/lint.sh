#!/usr/bin/env bash

exit_code=0

python_ver=$(python -c 'import sys; print("{}.{}".format(*sys.version_info[:2]))')

# Black and isort (latest version) don't support python 3.5.
if [ ! "$python_ver" == "3.5" ]; then
  black --check .
  exit_code=$(( $? | $exit_code ))

  isort --check-only .
  exit_code=$(( $? | $exit_code ))
fi

flake8 .
exit_code=$(( $? | $exit_code ))

exit $exit_code

import os

import pytest


@pytest.mark.parametrize("top_dir", ["mlflow_extend", "tests"])
def test_init_exists(top_dir: str) -> None:
    # mypy skips direcotries that do not contain `__init__.py`.
    # To prevent that, verify that `__init__.py` exists in all the directories.
    for root, _, files in os.walk(top_dir):
        if any(f.endswith(".py") for f in files):
            assert (
                "__init__.py" in files
            ), "`__init__.py` does not exist in `{}`".format(root)

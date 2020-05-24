import re

import mlflow_extend


def test_version_exists() -> None:
    assert hasattr(mlflow_extend, "__version__")


def test_version_format_is_valid() -> None:
    assert re.search(r"^\d+\.\d+\.\d+$", mlflow_extend.__version__) is not None

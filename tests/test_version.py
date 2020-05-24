import mlflow_extend
import re


def test_version_exists():
    assert hasattr(mlflow_extend, "__version__")


def test_version_format_is_valid():
    assert re.search(r"^\d+\.\d+\.\d+$", mlflow_extend.__version__) is not None

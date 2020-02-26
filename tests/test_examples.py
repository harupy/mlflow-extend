import pytest

from mlflow_extend.testing.utils import run_python_script


@pytest.mark.parametrize("path", ["examples/quickstart.py"])
def test_examples(path):
    assert run_python_script(path) == 0

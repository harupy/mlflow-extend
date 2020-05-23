import pytest

from mlflow_extend.testing.utils import _run_python_script


@pytest.mark.parametrize(
    "path", ["examples/quickstart.py", "examples/lightgbm_binary.py"]
)
def test_examples(path: str) -> None:
    assert _run_python_script(path) == 0

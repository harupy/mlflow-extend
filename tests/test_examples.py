import pytest

from tests.utils import run_python_script


@pytest.mark.parametrize("path", ["examples/quickstart.py"])
def test_examples(path):
    assert run_python_script(path) == 0

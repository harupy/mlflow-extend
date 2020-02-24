import pytest
from mlflow_extend import mlflow

from tests.utils import assert_file_exists_in_artifacts


@pytest.mark.parametrize("path", ["test.json", "dir/test.json", "dir/dir/test.json"])
def test_log_dict(path):
    with mlflow.start_run() as run:
        mlflow.log_dict({"a": 0}, path)
        assert_file_exists_in_artifacts(run, path)

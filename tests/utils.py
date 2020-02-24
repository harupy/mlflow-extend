import os
import mlflow


def assert_file_exists(path):
    assert os.path.exists(path)


def _list_artifacts(run_id, root=""):
    client = mlflow.tracking.MlflowClient()
    artifacts = []
    for artifact in client.list_artifacts(run_id, None if root == "" else root):
        if artifact.is_dir:
            next_root = os.path.join(artifact.path)
            artifacts += _list_artifacts(run_id, next_root)
        else:
            artifacts += [artifact.path]
    return artifacts


def assert_file_exists_in_artifacts(run, path):
    artifacts = _list_artifacts(run.info.run_id)
    assert path in artifacts

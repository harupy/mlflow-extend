import os
import subprocess
import inspect
import mlflow


def get_default_args(func):
    return {
        k: v.default
        for k, v in inspect.signature(func).parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def run_python_script(path):
    child = subprocess.Popen(
        ["export PYTHONPATH=$(pwd) && python {}".format(path)], shell=True
    )
    child.communicate()
    return child.returncode


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

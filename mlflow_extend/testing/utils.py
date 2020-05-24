import inspect
import json
import os
import subprocess
from typing import Any, Callable, Dict, List

import mlflow
import yaml
from matplotlib import pyplot as plt
from mlflow.entities.run import Run
from plotly import graph_objects as go


def _get_default_args(func: Callable[..., Any]) -> Dict[str, Any]:
    """
    Get default arguments of the given function.
    """
    return {
        k: v.default
        for k, v in inspect.signature(func).parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def _run_python_script(path: str) -> int:
    """
    Run a python script and return exit code.
    """
    child = subprocess.Popen(
        ["export PYTHONPATH=$(pwd) && python {}".format(path)], shell=True
    )
    child.communicate()
    return child.returncode


def _list_artifacts(run_id: str, root: str = "") -> List[str]:
    """
    List all artifacts in the specified run.
    """
    client = mlflow.tracking.MlflowClient()
    artifacts = []
    for artifact in client.list_artifacts(run_id, None if root == "" else root):
        if artifact.is_dir:
            next_root = os.path.join(artifact.path)
            artifacts += _list_artifacts(run_id, next_root)
        else:
            artifacts += [artifact.path]
    return artifacts


def _read_data(path: str) -> Dict[str, Any]:
    """
    Read data from JSON and YAML files.
    """
    with open(path, "r") as f:
        ext = os.path.splitext(path)[-1]
        if ext == ".json":
            return json.load(f)
        elif ext in [".yaml", ".yml"]:
            return yaml.load(f, Loader=yaml.SafeLoader)
        else:
            raise ValueError("Invalid file type: `{}`".format(ext))


def assert_is_figure(obj: Any) -> None:
    """
    Assert the given object is one of:
      - matplotlib.pyplot.Figure
      - plotly.graph_objects.Figure
    """
    assert isinstance(obj, (plt.Figure, go.Figure))


def assert_file_exists(path: str) -> None:
    """
    Assert the specified file exists.
    """
    assert os.path.exists(path)


def assert_file_exists_in_artifacts(run: Run, path: str) -> None:
    """
    Assert the specified file exists in the artifact store of the given run.
    """
    artifacts = _list_artifacts(run.info.run_id)
    assert path in artifacts


def assert_not_conflict_with_fluent_apis(new_apis: List[str]) -> None:
    """
    Assert new APIs mlflow_extend provides don't conflict the MLflow native APIs.
    """
    assert all(new_api not in mlflow.__all__ for new_api in new_apis)

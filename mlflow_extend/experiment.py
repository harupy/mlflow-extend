from typing import Optional

import mlflow

__all__ = ["get_or_create_experiment"]


def get_or_create_experiment(name: str, artifact_location: Optional[str] = None) -> str:
    """
    Get or create an experiment.

    Parameters
    ----------
        name : str
            Experiment name
        artifact_location : str, default None
            Location to store run artifacts. If unspecified, the server
            picks an appropriate default.

    Returns
    -------
    str
        ID of the experiment.

    Examples
    --------
    >>> with mlflow.start_run():
    ...     expr_id = mlflow.get_or_create_experiment('test')

    """
    expr = mlflow.get_experiment_by_name(name)
    if expr is None:
        return mlflow.create_experiment(name, artifact_location)

    return expr.experiment_id

import numpy as np
import py
import pytest

from mlflow_extend import plotting as mplt
from mlflow_extend.testing.utils import assert_is_figure
from mlflow_extend.typing import ArrayLike


@pytest.mark.parametrize("cm", [[[1, 2], [3, 4]], np.array([[1, 2], [3, 4]])])
def test_confusion_matrix(tmpdir: py.path.local, cm: ArrayLike) -> None:
    fig = mplt.confusion_matrix(cm)
    assert_is_figure(fig)


@pytest.mark.parametrize(
    "corr", [[[1.0, 2.0], [3.0, 4.0]], np.array([[1.0, 2.0], [3.0, 4.0]])]
)
def test_corr_matrix(tmpdir: py.path.local, corr: ArrayLike) -> None:
    fig = mplt.corr_matrix(corr)
    assert_is_figure(fig)


def test_feature_importance(tmpdir: py.path.local) -> None:
    features = ["a", "b", "c"]
    importances = [1, 2, 3]
    importance_type = "gain"
    fig = mplt.feature_importance(features, importances, importance_type)
    assert_is_figure(fig)


@pytest.mark.parametrize("limit", [2, 3, 4])
def test_feature_importance_with_limit(tmpdir: py.path.local, limit: int) -> None:
    features = ["a", "b", "c"]
    importances = [1, 2, 3]
    importance_type = "gain"
    fig = mplt.feature_importance(features, importances, importance_type, limit)
    assert_is_figure(fig)


def test_feature_importance_with_normalize(tmpdir: py.path.local) -> None:
    features = ["a", "b", "c"]
    importances = [1, 2, 3]
    importance_type = "gain"
    fig = mplt.feature_importance(
        features, importances, importance_type, normalize=True
    )
    assert_is_figure(fig)


def test_roc_curve(tmpdir: py.path.local) -> None:
    fig = mplt.roc_curve([1, 2, 3], [1, 2, 3])
    assert_is_figure(fig)

    fig = mplt.roc_curve([1, 2, 3], [1, 2, 3], 0.5)
    assert_is_figure(fig)


def test_pr_curve(tmpdir: py.path.local) -> None:
    fig = mplt.pr_curve([1, 2, 3], [1, 2, 3])
    assert_is_figure(fig)

    fig = mplt.pr_curve([1, 2, 3], [1, 2, 3], 0.5)

from typing import Optional

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from mlflow_extend.typing import ArrayLike

sns.set()

__all__ = [
    "corr_matrix",
    "confusion_matrix",
    "feature_importance",
    "roc_curve",
    "pr_curve",
]


def corr_matrix(corr: ArrayLike) -> plt.Figure:
    """
    Plot correlation matrix.

    Parameters
    ----------
    corr : array-like
        Correlation matrix.

    Returns
    -------
    matplotlib.pyplot.Figure
        Figure object.

    Examples
    --------
    .. plot::
        :context: close-figs

        >>> df = pd.DataFrame([(0.2, 0.3), (0.0, 0.6), (0.6, 0.0), (0.2, 0.1)],
        ...                   columns=['dogs', 'cats'])
        >>> corr_matrix(df.corr())  # doctest: +ELLIPSIS
        <Figure ... with 2 Axes>

    """
    fig, ax = plt.subplots()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask, k=1)] = True
    sns.heatmap(
        corr,
        vmin=-1,
        vmax=1,
        mask=mask,
        cmap=sns.diverging_palette(220, 10, as_cmap=True),
        linewidths=0.5,
        cbar=True,
        square=True,
        ax=ax,
    )
    ax.set_title("Correlation Matrix")
    fig.tight_layout()
    return fig


def confusion_matrix(
    cm: ArrayLike, labels: Optional[ArrayLike] = None, normalize: bool = True
) -> plt.Figure:
    """
    Plot confusion matrix.

    Parameters
    ----------
    cm : array-like
        Confusion matrix.
    labels : list of str, default None
        Label names.
    normalize : bool, default True
        Divide each row by its sum.

    Returns
    -------
    matplotlib.pyplot.Figure
        Figure object.

    Examples
    --------
    .. plot::
        :context: close-figs

        >>> cm = [[2, 0, 0],
        ...       [0, 0, 1],
        ...       [1, 0, 2]]
        >>> confusion_matrix(cm)  # doctest: +ELLIPSIS
        <Figure ... with 2 Axes>

    """
    cm = np.array(cm)
    cm_norm = cm / cm.sum(axis=1, keepdims=True)
    fig, ax = plt.subplots()
    sns.heatmap(
        cm_norm,
        cmap="Blues",
        vmin=0,
        vmax=1,
        fmt="s",
        annot=cm.astype(str),
        annot_kws={"fontsize": "large"},
        linewidths=0.2,
        cbar=True,
        square=True,
        ax=ax,
    )
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    ax.set_aspect("equal", adjustable="box")
    fig.tight_layout()
    return fig


def feature_importance(
    features: ArrayLike,
    importances: ArrayLike,
    importance_type: str,
    limit: Optional[int] = None,
    normalize: bool = False,
) -> plt.Figure:
    """
    Plot feature importance.

    Parameters
    ----------
    features : list of str
        Feature names.
    importances : array-like
        Importance of each feature.
    importance_type : str
        Feature importance type (e.g. "gain").
    limit : int, default None
        Number of features to plot. If ``None``, all features will be plotted.
    normalize : bool, default False
        Divide importance by the sum.

    Returns
    -------
    matplotlib.pyplot.Figure
        Figure object.

    Examples
    --------
    .. plot::
        :context: close-figs

        >>> features = ["a", "b", "c"]
        >>> importances = [1, 2, 3]
        >>> importance_type = "gain"
        >>> feature_importance(features, importances, importance_type)  # doctest: +ELLIPSIS
        <Figure ... with 1 Axes>

    """
    features = np.array(features)
    importances = np.array(importances)
    indices = np.argsort(importances)

    if limit is not None:
        indices = indices[-limit:]

    if normalize:
        importances = importances / importances.sum()

    features = features[indices]
    importances = importances[indices]
    num_features = len(features)
    bar_pos = np.arange(num_features)

    # Adjust the figure height to prevent the plot from becoming too dense.
    w, h = plt.rcParams["figure.figsize"]
    h += 0.1 * num_features if num_features > 10 else 0

    fig, ax = plt.subplots(figsize=(w, h))
    ax.barh(bar_pos, importances, align="center", height=0.5)
    ax.set_yticks(bar_pos)
    ax.set_yticklabels(features)
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    ax.set_title("Feature Importance ({})".format(importance_type))
    fig.tight_layout()
    return fig


def roc_curve(
    fpr: ArrayLike, tpr: ArrayLike, auc: Optional[float] = None
) -> plt.Figure:
    """
    Plot ROC curve.

    Parameters
    ----------
    fpr : array-like
        False positive rate.
    tpr : array-like
        True positive rate.
    auc : float, default None
        Area under the curve.

    Returns
    -------
    matplotlib.pyplot.Figure
        Figure object.

    Examples
    --------
    .. plot::
        :context: close-figs

        >>> fpr = np.linspace(0, 1, 11)
        >>> tpr = -((fpr - 1) ** 2) + 1
        >>> roc_curve(fpr, tpr)  # doctest: +ELLIPSIS
        <Figure ... with 1 Axes>

    """
    fig, ax = plt.subplots()
    ax.plot(fpr, tpr)
    ax.plot([0, 1], [0, 1], "k:")
    ax.set_xlabel("FPR")
    ax.set_ylabel("TPR")
    auc_str = "(AUC: {:.3f})".format(auc) if (auc is not None) else ""
    ax.set_title("ROC Curve" + auc_str)
    fig.tight_layout()
    return fig


def pr_curve(pre: ArrayLike, rec: ArrayLike, auc: Optional[float] = None) -> plt.Figure:
    """
    Plot precision-recall curve.

    Parameters
    ----------
    pre : array-like
        Precision.
    rec : array-like
        Recall.
    auc : float, default None
        Area under the curve.

    Returns
    -------
    matplotlib.pyplot.Figure
        Figure object.

    Examples
    --------
    .. plot::
        :context: close-figs

        >>> rec = np.linspace(0, 1, 11)
        >>> pre = -(rec ** 2) + 1
        >>> pr_curve(pre, rec)  # doctest: +ELLIPSIS
        <Figure ... with 1 Axes>

    """

    fig, ax = plt.subplots()
    ax.plot(rec, pre)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Presision")
    auc_str = " (AUC: {:.3f})".format(auc) if (auc is not None) else ""
    ax.set_title("Precision-Recall Curve " + auc_str)
    fig.tight_layout()
    return fig

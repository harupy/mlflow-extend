from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from mlflow_extend.typing import ArrayLike

sns.set()


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
        Matplotlib figure instance.

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
        Matplotlib figure instance.

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
        annot=cm_norm.round(2).astype(str),
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
        Matplotlib figure instance.

    """
    features = np.array(features)
    importances = np.array(importances)
    indices = np.argsort(importances)

    if limit is not None:
        indices = indices[-limit:]

    if normalize:
        importances = importances / importances.sum()

    y = np.arange(len(features[indices]))
    fig, ax = plt.subplots()
    ax.barh(y, importances[indices], align="center", height=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(features[indices])
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
        Matplotlib figure instance.

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
        Matplotlib figure instance.

    """
    fig, ax = plt.subplots()
    ax.plot(rec, pre)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Presision")
    auc_str = " (AUC: {:.3f})".format(auc) if (auc is not None) else ""
    ax.set_title("Precision-Recall Curve " + auc_str)
    fig.tight_layout()
    return fig

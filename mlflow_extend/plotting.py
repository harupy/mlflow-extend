import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


def corr_matrix(corr):
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


def confusion_matrix(cm, labels=None, normalize=True):
    cm_norm = cm / cm.sum(axis=1, keepdims=True)
    fig, ax = plt.subplots()
    sns.heatmap(
        cm_norm,
        cmap="Blues",
        vmin=0,
        vmax=1,
        fmt="s",
        annot=cm_norm,
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


def feature_importance(features, importances, importance_type, limit=None):
    features = np.array(features)
    importances = np.array(importances)
    indices = np.argsort(importances)
    y = np.arange(len(importances))

    if limit is not None:
        indices = indices[-limit:]

    fig, ax = plt.subplots()
    ax.barh(y, importances[indices], align="center", height=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(features[indices])
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    ax.set_title("Feature Importance ({})".format(importance_type))
    fig.tight_layout()
    return fig


def roc_curve(fpr, tpr, auc=None):
    fig, ax = plt.subplots()
    ax.plot(fpr, tpr)
    ax.plot([0, 1], [0, 1], "k:")
    ax.set_xlabel("FPR")
    ax.set_ylabel("TPR")
    auc_str = "(AUC: {:.3f})".format(auc) if (auc is not None) else ""
    ax.set_title("ROC Curve" + auc_str)
    fig.tight_layout()
    return fig


def pr_curve(pre, rec, auc=None):
    fig, ax = plt.subplots()
    ax.plot(pre, rec)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Presision")
    auc_str = " (AUC: {:.3f})".format(auc) if (auc is not None) else ""
    ax.set_title("Precision-Recall Curve " + auc_str)
    fig.tight_layout()
    return fig

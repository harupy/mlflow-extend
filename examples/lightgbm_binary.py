"""
An example script to train a LightGBM classifier on the breast cancer dataset.

The lines that call mlflow_extend APIs are marked with "EX".
"""
import lightgbm as lgb
import pandas as pd
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from mlflow_extend import mlflow


def breast_cancer():
    data = datasets.load_breast_cancer()
    columns = list(filter(lambda c: c.replace(" ", "_"), data.feature_names))
    X = pd.DataFrame(data.data, columns=columns)
    y = pd.Series(data.target, name="target")
    return X, y


def main():
    config = {
        "split": {"test_size": 0.2, "random_state": 42},
        "model": {"objective": "binary", "metric": "auc", "seed": 42},
        "fit": {"num_boost_round": 10, "early_stopping_rounds": 3},
    }
    # Prepare training data.
    X, y = breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(X, y, **config["split"])
    train_set = lgb.Dataset(X_train, label=y_train)

    # Set experiment.
    expr_name = "lightgbm"
    mlflow.get_or_create_experiment(expr_name)  # EX
    mlflow.set_experiment(expr_name)

    with mlflow.start_run():
        # Log training configuration.
        mlflow.log_params_flatten(config)  # EX
        mlflow.log_dict(config, "config.json")  # EX

        # Train model.
        model = lgb.train(
            config["model"],
            train_set,
            valid_sets=[train_set],
            valid_names=["train"],
            **config["fit"]
        )

        # Log feature importance.
        importance_type = "gain"
        features = model.feature_name()
        importances = model.feature_importance(importance_type)
        mlflow.log_feature_importance(features, importances, importance_type)  # EX

        # Log confusion metrics.
        mlflow.log_metrics_flatten(model.best_score)

        # Log confusion matrix.
        y_proba = model.predict(X_test)
        cm = confusion_matrix(y_test, y_proba > 0.5)
        mlflow.log_confusion_matrix(cm)  # EX


if __name__ == "__main__":
    main()

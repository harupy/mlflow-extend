import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mlflow_extend import mlflow


def main():
    with mlflow.start_run():
        # mlflow native APIs
        mlflow.log_param("param", 0)
        mlflow.log_metric("metric", 1.0)

        # flatten dict
        mlflow.log_params_flatten({"a": {"b": 0}})
        mlflow.log_metrics_flatten({"a": {"b": 0.0}})

        # dict
        mlflow.log_dict({"a": 0}, "dict.json")

        # numpy array
        mlflow.log_numpy(np.array([0]), "array.npy")

        # pandas dataframe
        mlflow.log_df(pd.DataFrame({"a": [0]}), "df.csv")

        # matplotlib figure
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1])
        mlflow.log_figure(fig, "figure.png")

        # confusion matrix
        mlflow.log_confusion_matrix([[1, 2], [3, 4]])


if __name__ == "__main__":
    main()

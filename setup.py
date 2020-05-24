import os
from typing import List

from setuptools import find_packages, setup

import mlflow_extend

ROOT = os.path.abspath(os.path.dirname(__file__))
GITHUB_REPO_URL = "https://github.com/harupy/mlflow-extend"


def get_readme() -> str:
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        return f.read()


def get_install_requires() -> List[str]:
    with open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8") as f:
        return [
            line.strip()
            for line in f.readlines()
            if not (line.startswith("#") or (line.strip() == ""))
        ]


setup(
    name="mlflow-extend",
    version=mlflow_extend.__version__,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=get_install_requires(),
    maintainer="harupy",
    maintainer_email="hkawamura0130@gmail.com",
    url=GITHUB_REPO_URL,
    project_urls={
        "Documentation": "https://mlflow-extend.readthedocs.io/en/latest/index.html",
        "Source Code": GITHUB_REPO_URL,
        "Bug Tracker": os.path.join(GITHUB_REPO_URL, "issues"),
    },
    description="Extend MLflow's functionality",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)

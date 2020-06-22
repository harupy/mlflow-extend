from setuptools import setup

from version import __version__
import bare_pytest_raises

setup(
    name="flake8-extensions",
    version=__version__,
    zip_safe=False,
    py_modules=["bare_pytest_raises"],
    install_requires=["flake8"],
    entry_points={
        "flake8.extension": [
            (
                f"{bare_pytest_raises.ERROR_CODE_LETTER} "
                "= bare_pytest_raises:BarePytestRaises"
            )
        ]
    },
)

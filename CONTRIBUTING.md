# Contributing

## Creating a development environment

```bash
conda create -n mlflow-extend python=3.6
conda activate mlflow-extend
pip install -r requirements.txt -r requirements-dev.txt
```

## Check code format

```bash
./dev/lint.sh
```

## Running type check

```bash
mypy .
```

## Running unit tests

```bash
# Run all the unit tests.
./dev/test.sh

# Save figures generated during the unit tests in '.pytest_basetemp'.
./dev/test.sh --savefig
```

## Building documentation

```bash
cd docs
make html

# Remove everything under 'docs/build' and run 'make html'.
make clean html
```

The generated files will be stored in `docs/build/html`. Open `docs/build/html/index.html` on the browser to check if the documentation is built properly.

## Releasing a new version

1. Make a pull request to update `__version__` in `mlflow-extend/version.py` to the next version.

```diff
- __version__ = "1.2.2"  # current version
+ __version__ = "1.2.3"  # next version
```

2. After the pull request is merged, create a new tag and push it to the remote.

```bash
git tag v1.2.3
git push origin v1.2.3
```

3. Open [the release page](https://github.com/harupy/mlflow-extend/releases) and publish a new release.

4. Upload distribution archives to PyPI using [twine](https://github.com/pypa/twine#using-twine).

```bash
# Remove old distribution archives.
rm -r dist/*

# Generate new distribution archives.
python setup.py sdist bdist_wheel

# Upload to Test PyPI and verify everything looks right.
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Upload to PyPI (THIS CAN NOT BE UNDONE).
twine upload dist/*
```

# ValidMind Python Client

## Contributing to ValidMind Developer Framework

### Install dependencies

- Ensure you have `poetry` installed: https://python-poetry.org/

- After cloning this repo run:

```
poetry shell
poetry install
```

### Versioning

Make sure you bump the package version before merging a PR with the following command:

```
make version tag=prerelease
```

The value of `tag` corresponds to one of the options provided by Poetry: https://python-poetry.org/docs/cli/#version

## Integrating the ValidMind Developer Framework to your development environment

If you want to integate the `validmind` package to your development environment, you must build the package
wheel first, since we have not pushed the package to a public PyPI repository yet. Steps:

- Run `make build` to build a new Python package for the developer framework
- This will create a new wheel file in the `dist` folder
- Run `pip install <path-to-wheel>` to install the newly built package in your environment

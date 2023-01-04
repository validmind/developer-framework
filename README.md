# ValidMind Python Client

## Integrating the ValidMind Developer Framework to your development environment

Run `make build` to build a new Python package for the SDK. Pushing
to a PyPI repository is work in progress.

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

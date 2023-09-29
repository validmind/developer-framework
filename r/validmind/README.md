# Validmind R Package

This package is under **heavy development** and should not be relied on for production use at this point!

## Installation

1. Set your working directory to the root folder of the r package
2. Install the `devtools` package with the following command:

```r
install.packages("devtools")
```

3. Now install `validmind` with the following command:

```r
devtools::install()
```

4. Confirm the installation was successful with:

```r
library(validmind)
```

## Quick Start

You can connect to your ValidMind profile by providing the appropriate credentials:

```r
vm_r <- vm(
  api_key="<your_api_key_here>",
  api_secret="<your_api_secret_here>",
  project="<your_project_id_here>",
  python_version="<path_to_your_python_version_here>",
  api_host="https://api.dev.vm.validmind.ai/api/v1/tracking"
)
```

## Fleshed out Example

Coming soon...

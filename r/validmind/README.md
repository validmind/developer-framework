# ValidMind R Package

## Installation

You can install ValidMind from CRAN:

```r
install.packages("validmind")
```

You can also install the package from GitHub using the `devtools` package:

```r
devtools::install_github("validmind/developer-framework", subdir="r/validmind")
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

Please see the `notebooks/code-sharing/r` folder for examples of how to use!

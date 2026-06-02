#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_name="${TTN_CONDA_ENV:-ttn-env}"

if ! command -v conda >/dev/null 2>&1; then
    echo "conda was not found in PATH. Activate Miniconda/Anaconda first or add conda to PATH." >&2
    exit 1
fi

export PYTHONPATH="${project_root}/src"
cd "${project_root}"

conda_prefix="$(conda run -n "${env_name}" python -c 'import os; print(os.environ["CONDA_PREFIX"])')"
export PROJ_LIB="${conda_prefix}/share/proj"
export PROJ_DATA="${PROJ_LIB}"

conda run -n "${env_name}" python -m thucthengay "$@"

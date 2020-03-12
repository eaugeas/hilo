#!/bin/bash -e

VENV=".venv"

function has_nvidia_gpu() {
    if [ -z "$(command -v nvidia-smi)" ]; then
        echo "0"
        return
    fi

    GPU_COUNT=$(nvidia-smi -L | wc -l)
    if [ "$GPU_COUNT" == "0" ]; then
        echo "0"
        return
    fi

    echo "1"
}

# set up python environment if it doesn't exist
if [ ! -d "$VENV" ]; then
    PYTHON3=$(command -v python3)
    VIRTUALENV=$(command -v virtualenv)

    if [ -z "$PYTHON3" ]; then
        echo "Make sure python3 is installed in the system."
        exit 1
    fi

    if [ -z "$VIRTUALENV" ]; then
        echo "Make sure virtualenv is installed in the system."
        exit 1
    fi

    GPU=$(has_nvidia_gpu)
    $VIRTUALENV -p "$PYTHON3" .venv
    source "$VENV"/bin/activate

    # install dependencies based on whether GPU support
    # is available
    if [ "$GPU" == "1" ]; then
        pip install -r requirements_gpu.txt
    else
        pip install -r requirements_nongpu.txt
    fi
fi

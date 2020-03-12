#!/usr/bin/env bash

VENV=".venv"

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

    $VIRTUALENV -p "$PYTHON3" .venv
    source "$VENV"/bin/activate

    pip install -r requirements.txt
fi

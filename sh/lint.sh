#!/bin/sh
lint() {
    echo "Linting '$1'..."
    black --quiet --check "$1"
    if [ "$?" -ne "0" ]; then
        echo "black - failed" >&2
        exit 1
    else
        echo "black - passed"
    fi

    flake8 --quiet "$1"
    if [ "$?" -ne "0" ]; then
        echo "flake8 - failed" >&2
        exit 1
    else
        echo "flake8 - passed"
    fi

    isort --check "$1" >/dev/null
    if [ "$?" -ne "0" ]; then
        echo "isort - failed" >&2
        exit 1
    else
        echo "isort - passed"
    fi

    mypy "$1" >/dev/null
    if [ "$?" -ne "0" ]; then
        echo "mypy - failed" >&2
        exit 1
    else
        echo "mypy - passed"
    fi
}

lint functions
lint tests

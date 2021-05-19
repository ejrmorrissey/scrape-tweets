#! /bin/#!/usr/bin/env bash

# cd to Dockerfile directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "${SCRIPT_DIR}" || exit

pipenv --python 3
pipenv run pip3 install --upgrade pip

cd ./services/web || exit
pipenv run pip3 install -r requirements.txt
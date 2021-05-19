#! /bin/#!/usr/bin/env bash

# cd to Dockerfile directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "${SCRIPT_DIR}" || exit

cd ./services/web || exit
pip3 install -r requirements.txt --user
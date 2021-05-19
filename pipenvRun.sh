#! /bin/#!/usr/bin/env bash

# cd to Dockerfile directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "${SCRIPT_DIR}" || exit

cd ./services/web || exit
pipenv run python3 manage.py run "${TWEET_SCRAPER_HANDLE}"
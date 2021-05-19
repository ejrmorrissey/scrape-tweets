#! /bin/#!/usr/bin/env bash

# cd to Dockerfile directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "${SCRIPT_DIR}" || exit
cd services || exit

# build image
docker build --tag ubuntu:bionic .

# Run image, mapping port 5000 of container to 5000 of host, mounting /services/web as a volume and starting up app
docker run --name tweet-scraper -p 5000:5000 -v \
"${SCRIPT_DIR}"/services/web:/usr/src/app/ --env-file ../.env.dev ubuntu:bionic \
python3 manage.py run "${TWEET_SCRAPER_HANDLE}"


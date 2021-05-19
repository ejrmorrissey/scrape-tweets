# scrape-tweets

## Description
This app scrapes the most recent tweets from a given account and prints them to stdout, and then polls the timeline once every 10 minutes for new tweets.

The project is written in Python, uses Selenium for scraping and runs a Flask server which exposes a few APIs (see Usage).

## Installation
Although this app should run on Windows in containerised or non-containerised form, the instructions here are for *nix systems.

The easiest way to ensure your environment is set up to run the app is to run inside a container. **Note: The image created will be large (hundreds of mb) as it includes everything needed to run Selenium.**

### Docker Compose

Requirements:
- docker-compose installed
- port 5000 is available
- sufficient storage for docker image

From the root directory of the project run the following command:

`export TWEET_SCRAPER_HANDLE=twitter-handle && docker-compose build && docker-compose up`

Where *twitter-handle* is the handle of the account to monitor. E.g.

`export TWEET_SCRAPER_HANDLE=reuters && docker-compose build && docker-compose up`



## Usage

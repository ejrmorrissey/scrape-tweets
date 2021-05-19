# scrape-tweets

## Description
This app scrapes the most recent tweets from a given account and prints them to stdout, and then polls the timeline once every 10 minutes for new tweets.

The project is written in Python, uses Selenium for scraping and runs a Flask server which exposes a few APIs (see Usage).

## Install and Run
Although this app should run on Windows in containerised or non-containerised form, the instructions here are for *nix systems.

The easiest way to ensure your environment is set up to run the app is to run inside a container. **Note: The image created will be large (hundreds of mb) as it includes everything needed to run Selenium in a container.**

### Docker

Requirements:
- docker installed
- port 5000 is available
- sufficient storage for docker image
- internet access for pulling image etc
- app process will need write permissions for its own directory

The script runDocker.sh is provided to make starting the app with docker simple. It requires the environment variable *TWEET_SCRAPER_HANDLE* to be exported with the value of the handle of account to be monitored. For example run the following command from the project root,

`export TWEET_SCRAPER_HANDLE=twitter-handle && sh runDocker.sh`

Where *twitter-handle* is the handle of the account to monitor. E.g.

`export TWEET_SCRAPER_HANDLE=reuters && sh runDocker.sh`

To start up the app subsequently, run

`docker start tweet-scraper -a`

The -a flag attaches to container to stdout.

### Docker Compose

Requirements:
- docker-compose installed
- port 5000 is available
- sufficient storage for docker image
- internet access for pulling image etc
- app process will need write permissions for its own directory

From the root directory of the project run the following command:

`export TWEET_SCRAPER_HANDLE=twitter-handle && docker-compose build && docker-compose up`

To start up the app subsequently, run `docker-compose up` in the project root.

## Usage
Regardless of which method you choose to run the app, it will print tweets to stdout. Initially 5 tweets should be printed (possibly with intermediate loading if required), and then every 10 minutes the feed will be polled for new tweets.

With the above methods for running, a couple of control-c's should kill the app.

The app server will be available on http://localhost:5000. To retrieve a list of all tweets scraped during the app's runtime, use a get request with the endpoint /addTweets. For example,

`curl http://localhost:5000/allTweets`


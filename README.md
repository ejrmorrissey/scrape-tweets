# scrape-tweets

## Description
This app scrapes the most recent tweets from a given account and prints them to stdout, and then polls the timeline once every 10 minutes for new tweets.

The project is written in Python3, uses Selenium for scraping and runs a Flask server which exposes a few APIs (see Usage).

## Install and Run
Although this app should run on Windows in containerised or non-containerised form, the instructions here are for *nix systems.

The easiest way to ensure your environment is set up to run the app is to run inside a container. However, with this method the image and container will need to be removed and built again in order to change the twitter account that app monitors. With a pipenv or python deployment the twitter account followed can be set every time the app is run.

**Note: When running with a container image created will be large (hundreds of mb) as it includes everything needed to run Selenium.**

**In all of the following commands, substitute 'twitter-handle' for the handle of the account you wish to monitor. E.g. 'reuters'**

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

### Pipenv

Requirements
- Python3 environment set up with pipenv
- port 5000 is available
- internet access for installing packages
- app process will need write permissions for its own directory
- possibly Firefox installed, geckodriver available

Some scripts are provided to make pipenv deployment easier. On first starting the app run:

`export TWEET_SCRAPER_HANDLE=twitter-handle && sh pipenvSetup.sh && sh pipenvRun.sh`

Subsquently you can run,

`export TWEET_SCRAPER_HANDLE=twitter-handle && sh pipenvRun.sh`

Unlike a containerised deployment, the twitter handle can be set anew each time the app is started.

Running the app with this method may require Firefox to be installed in your environment, and the firefox geckdodriver for selenium may need to be installed separately. Some methods of doing this are contained in these threads,

[https://stackoverflow.com/questions/41190989/how-do-i-install-geckodriver](https://stackoverflow.com/questions/41190989/how-do-i-install-geckodriver)

[https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu)


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

### Straightforward Python

Requirements
- python3 and pip3 available as commands
- port 5000 is available
- internet access for installing packages
- app process will need write permissions for its own directory
- possibly Firefox installed, geckodriver available

This is perhaps the least recommended method of running the app as it's most dependent on the host environment. All of the requirements for the Pipenv method also apply, and python3 and pip3 must be available as commands.

On first starting the app run:

`export TWEET_SCRAPER_HANDLE=twitter-handle && sh pythonSetup.sh && sh pythonRun.sh`

Subsquently you can run,

`export TWEET_SCRAPER_HANDLE=twitter-handle && sh pythonRun.sh`

## Usage
Regardless of which method you choose to run the app, it will print tweets to stdout. Initially 5 tweets should be printed (possibly with intermediate loading if required), and then every 10 minutes the feed will be polled for new tweets.

With the above methods for running, a couple of control-c's should kill the app.

The app server will be available on http://localhost:5000. To retrieve a list of all tweets scraped during the app's runtime, use a get request with the endpoint /addTweets. For example,

`curl http://localhost:5000/allTweets`


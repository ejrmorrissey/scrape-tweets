import time
from collections import OrderedDict
import json

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from main import app

from main.tweet import Tweet

SERIALISED_FILE_PATH = app.config["SERIALISED_FILE_PATH"]
RESOURCES_PATH = app.config["RESOURCES_PATH"]

TWEETS_XPATH = "//*[@data-testid='tweet']"
TEXT_REL_XPATH = "/div[2]/div[2]/div[1]"
HEADER_REL_XPATH = "/div[2]/div[1]/div[1]/div[1]/div[1]"
HEADER_TWEETER_REL_XPATH = "/div[1]"
HEADER_DATE_ID = "/a"
PINNED_REL_XPATH = "/../div[1]//*[text()='Pinned Tweet']"


class Scraper:

    #handle = "reuters"

    def __init__(self):
        #self.handle = app.config["handle"]
        opts = Options()
        opts.headless = True
        self.browser = Firefox(options=opts)
        self.all_tweets = OrderedDict()

    def refresh(self):
        self.browser.get(f"https://twitter.com/{app.config['handle']}")

    def _get_tweet_elements(self):
        """
        Scrape tweet elements from feed using xpath selector
        :return: a list of tweet elements
        """

        tweet_elements = self.browser.find_elements_by_xpath(TWEETS_XPATH)
        loop_counter = 0
        # Ensure tweets have loaded
        while len(tweet_elements) == 0:
            if loop_counter == 60:
                print("No more tweets found on page")
                return []
            loop_counter += 1
            time.sleep(1)
            tweet_elements = self.browser.find_elements_by_xpath(TWEETS_XPATH)
        tweet_elements.reverse()
        return tweet_elements

    def _element_to_tweet(self, element):
        """
        Convert scraped tweet element to Tweet object: containing the status url, account handle and name,
        date of tweet, text and a boolean for whether the tweet is pinned.
        :param element: node scraped from feed
        :return: Tweet object from element
        """
        tweeter = element.find_element_by_xpath(f".{HEADER_REL_XPATH}{HEADER_TWEETER_REL_XPATH}").text
        status_link = element.find_element_by_xpath(f".{HEADER_REL_XPATH}{HEADER_DATE_ID}")
        tweet_date = status_link.text
        tweet_id = status_link.get_attribute("href")
        text = element.find_element_by_xpath(f".{TEXT_REL_XPATH}").text
        try:
            element.find_element_by_xpath(f".{PINNED_REL_XPATH}")
            pinned = True
        except NoSuchElementException:
            pinned = False
        return Tweet(status_id=tweet_id, account=tweeter, date_string=tweet_date, text=text, pinned=pinned)

    def _scrape_tweets(self):
        """
        Scrape tweets from feed using xpath selectors, convert to Tweet objects for holding data and filter out
        pinned tweets which are chronologically earlier than preceding tweets.
        :return: a list of Tweet objects
        """
        tweet_elements = self._get_tweet_elements()
        tweets = self._filter_pinned_tweets([self._element_to_tweet(element) for element in tweet_elements])
        return tweets

    def _filter_pinned_tweets(self, tweets):
        """
        Filter out pinned tweets which aren't chronologically newer than tweets further down in feed.
        :param tweets: list of tweets
        :return: list of tweets with old pinned tweets filtered out
        """
        new_tweets_list = []
        while len(tweets) > 1:
            tweet = tweets.pop()
            if tweet.pinned:
                if tweet.date < tweets[-1].date:
                    continue
            new_tweets_list.append(tweet)
        # Final tweet in list is simply added as we don't have the tweets further down in feed for comparison
        new_tweets_list.append(tweets.pop())
        del tweets
        return new_tweets_list

    def _scroll_timeline(self):
        """
        Scroll down browser window to load more tweets
        :return: Boolean representing whether or not we've reached end of feed
        """
        previous_height = self.browser.execute_script("return document.body.scrollHeight")
        # Scroll by 20% of window height so as not to miss any tweets
        self.browser.execute_script(f"window.scrollTo(0, {0.2*previous_height});")
        wait_counter = 0
        end_of_feed = self.browser.execute_script("return document.body.scrollHeight") == previous_height
        # ensure the scrolled page has time to load
        while end_of_feed:
            wait_counter += 1
            time.sleep(1)
            # if the scollHeight hasn't changed after scrolling, we've reached end of feed
            end_of_feed = self.browser.execute_script("return document.body.scrollHeight") == previous_height
            if wait_counter == 60:
                break
        return end_of_feed

    def _write_serialised(self, tweets):
        """
        Serialise tweets to file as json list of objects
        :param tweets: list of Tweet objects
        """
        with open(SERIALISED_FILE_PATH, "w+") as file:
            json_string = json.dumps([tweet.as_dict() for tweet in tweets])
            file.write(json_string)

    def _load_serialised(self):
        """
        Load serialised tweets from file
        :return: a list of deserialised Tweet objects
        """
        with open(SERIALISED_FILE_PATH, "r") as file:
            tweets_json = json.loads(file.read())
            return [Tweet.from_json(tweet_json) for tweet_json in tweets_json]

    def _load_serialised_json(self):
        """
        Load serialised tweets from file as json
        :return: a list of json objects
        """
        keys = ["status", "user", "date", "text"]
        with open(SERIALISED_FILE_PATH, "r") as file:
            return [{k: tweet[k] for k in keys} for tweet in json.loads(file.read())]

    def _print_latest_tweets(self, tweets):
        """
        Print tweets using the original time string they were scraped with--this could be a full date or in the form
        of hours ago etc.
        :param tweets: Tweet objects to print
        """
        print(*[f"\n{tweet.as_text_with_date_string()}\n" for tweet in tweets])

    def get_feed(self):
        """
        Print out the top 5 tweets from a feed, excluding old pinned tweets. If less than 5 are scraped initially,
        attempt to scroll down to load more.
        """
        print(f"Loading {app.config['handle']}'s feed, this may take a few moments...")
        self.refresh()
        tweets = self._scrape_tweets()
        # Keep a set of tweet status ids to prevent scraping tweets which have already been loaded
        loaded_statuses = set([tweet.status_id for tweet in tweets])
        self._print_latest_tweets(tweets)
        # The number of tweets scraped initially
        num_printed = len(tweets)
        while num_printed < 5:
            print("Still loading tweets...")
            bottom_of_page = self._scroll_timeline()
            additional_tweets = [tweet for tweet in self._scrape_tweets() if tweet.status_id not in loaded_statuses]
            loaded_statuses.update([tweet.status_id for tweet in additional_tweets])
            if len(additional_tweets) > 0:
                # Make up the difference between 5 and the number of tweets already printed
                num_to_print = 5 - num_printed
                self._print_latest_tweets(additional_tweets[:num_to_print])
                num_printed += num_to_print
                # All tweets we scrape are stored, including those beyond the 5 printed.
                tweets.extend(additional_tweets)
            if bottom_of_page:
                print("No more tweets were found.")
                break
        self._write_serialised(tweets)
        return

    def update_feed(self):
        """
        This method called periodically to print any new tweets in feed since initial scraping.
        """
        print("Checking for new tweets...")
        all_tweets = self._load_serialised()
        # load a set of all tweets previously stored to avoid scraping the same tweets multiple times
        loaded_statuses = set([tweet.status_id for tweet in all_tweets])
        self.refresh()
        counter = 0
        loaded = False
        new_tweets = []
        # Since refresh has just been called, we may need to wait for the page to reload
        while loaded is False and counter < 60:
            try:
                new_tweets = [tweet for tweet in self._scrape_tweets() if
                              tweet.status_id not in loaded_statuses and tweet.date > all_tweets[-1].date]
                loaded = True
            except StaleElementReferenceException:
                counter += 1
                time.sleep(0.5)
        all_tweets.extend([tweet for tweet in new_tweets])
        loaded_statuses.update([tweet.status_id for tweet in new_tweets])
        page_scrolls = 0
        bottom_of_page = False
        while len(new_tweets) > 0:
            self._print_latest_tweets(new_tweets)
            # Set an arbitrary limit on page scrolls performed in order to load new tweets. If the user has made a huge
            # amount of tweets since initial load, they may not all be scraped. However this will also stop the app
            # from scraping indefinitely if we somehow accidentally scroll past all previously loaded tweets.
            if bottom_of_page or page_scrolls > 10:
                return
            bottom_of_page = self._scroll_timeline()
            page_scrolls += 1
            # Ensure that the newly scraped tweets are chronologically later than the most recent tweet from the last
            # load. There may be unexpected behaviour is the user has made a large amount of tweets since initial load
            # and these include retweets which aren't in chronological order. However this is an edge case.
            new_tweets = [tweet for tweet in self._scrape_tweets()
                          if tweet.status_id not in loaded_statuses and tweet.date > all_tweets[-1].date]
            all_tweets.extend([tweet for tweet in new_tweets])
            loaded_statuses.update([tweet.status_id for tweet in new_tweets])
        self._write_serialised(all_tweets)
        return

    def fetch_tweets(self):
        """
        Return all stored tweets as json
        :return: list of tweet objects, in json form
        """
        return self._load_serialised_json()



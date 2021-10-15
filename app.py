#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import threading
import time
from typing import List

import reddit
import twitter
from branding import SelfBrand
from logger import logger


def run_bot():
    twitter_credentials = twitter.TwitterCredentials.read_from_json_file(
        "credentials.json"
    )
    twitter_bot = twitter.TwitterBot(twitter_credentials)

    reddit_credentials = reddit.RedditCredentials.read_from_json_file(
        "credentials.json"
    )
    reddit_scrapper = reddit.SubredditScrapper(reddit_credentials)

    posts: List[reddit.RedditPost] = []

    failures_counter = 0

    while failures_counter < 3:

        posts.extend(reddit_scrapper.fetch_posts())

        # re-fetch when no posts is available
        if not len(posts):
            logger.warning("increase failure counter")
            failures_counter += 1

            logger.warning("Sleep for 15 min before fetching again")
            time.sleep(60 * 15)
            continue
        else:
            logger.info("reset failure counter")
            failures_counter = 0

        # share posts
        while len(posts):
            post = posts.pop(0)
            media_filename = post.download_media()

            twitter_bot.tweet(post.content, media_filename)

            time.sleep(60 * 15)


def run_branding():
    twitter_credentials = twitter.TwitterCredentials.read_from_json_file(
        "credentials.json"
    )
    branding_bot = SelfBrand(twitter_credentials)

    hashtags = ["#reddit", "#memes"]

    for hashtag in hashtags:
        tweets = branding_bot.fetch_tweets_from_hashtag(hashtag, 90)
        logger.info("Fetched {} tweets from hashtag {}".format(len(tweets), hashtag))

        branding_bot.fav_tweets(tweets)
        logger.info("Liked all tweet from hashtag {}".format(hashtag))


def main():
    print("Running ...")

    branding_bot = threading.Thread(target=run_branding)
    branding_bot.setDaemon(True)
    branding_bot.start()

    run_bot()
    print("Finished")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping ...")

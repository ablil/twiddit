#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-14

import time
from typing import List

import tweepy

from logger import logger


class SelfBrand:

    hashtags = ["#meme", "#memes", "#reddit"]
    tweets_per_hashtag = 10

    def __init__(self, key, secret, token_key, token_secret):
        self.auth = tweepy.OAuthHandler(key, secret)
        self.auth.set_access_token(token_key, token_secret)
        self.api = tweepy.API(self.auth)

    def run(self):
         while True:
            try:
                for hashtag in SelfBrand.hashtags:
                    tweets = self.__fetch_some_tweets(hashtag)
                    logger.info(
                        "Fetched {} tweets with hashtag {}".format(len(tweets), hashtag)
                    )

                    self.__like_tweets(tweets)
                    logger.info(
                        "liked all {} tweets from hashtag {}".format(
                            len(tweets), hashtag
                        )
                    )

            except Exception as e:
                logger.warning("could not continue execution of self-branding")
                logger.warning(e)

            finally:
                time.sleep(60 * 5)

    def __fetch_some_tweets(self, hashtag) -> List[tweepy.models.Status]:
        tweets = tweepy.Cursor(self.api.search_tweets, q=hashtag, lang="en").items(
            SelfBrand.tweets_per_hashtag
        )

        return list(tweets)

    def __like_tweets(self, tweets: tweepy.models.Status):
        failures = 0
        for tweet in tweets:
            try:
                self.api.create_favorite(tweet.id)
            except Exception as e:
                failures += 1

        if failures:
            logger.warning("Some tweets are already liked !!!")

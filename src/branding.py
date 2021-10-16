#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-14

import time
from typing import List

import tweepy

from logger import logger
from twitter import TwitterCredentials


class SelfBrand:
    def __init__(self, credentials: TwitterCredentials):
        self.credentials = credentials
        self.api = self.credentials.api

    def fav_tweets(self, tweets_ids: List[int], interval: int = 60):
        """like all tweets every interval in seconds

        Args:
            tweets_ids (List[int]): tweets ids
            interval (int, optional): intervale between like in seconds. Defaults to 60.
        """

        i = 0
        while i < len(tweets_ids):
            try:
                self.api.create_favorite(tweets_ids[i])
                logger.info("Liked tweet with id {}".format(tweets_ids[i]))
            except tweepy.TwitterServerError as e:
                logger.error(e)
            except tweepy.errors.Forbidden as e:
                logger.error(e)

            i += 1
            time.sleep(interval)

    def fetch_tweets_from_hashtag(
        self, hashtag: str, limit: int = 50
    ) -> List[int]:
        """Fetch recent tweet from given hashtag

        Args:
            hashtag (str): twitter hashtag

        Returns:
            List[int]: list of tweets ids
        """
        if not hashtag.startswith("#"):
            hashtag = "#" + hashtag

        if not limit or limit > 100 or limit < 10:
            limit = 50

        tweets = tweepy.Cursor(self.api.search_tweets, q=hashtag).items(limit)
        unliked = filter(lambda t: not t.favorited, tweets)
        ids = map(lambda t: t.id, unliked)
        return list(ids)

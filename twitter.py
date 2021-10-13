#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import os
from typing import List
import tweepy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Bot:
    def __init__(self, key, secret, token_key, token_secret):
        self.auth = tweepy.OAuthHandler(key, secret)
        self.auth.set_access_token(token_key, token_secret)
        self.api = tweepy.API(self.auth)
        logger.info("connected to twitter api")

    def post(self, content: str, filename: str):
        assert os.path.exists(filename)

        logger.info("started posting tweet")
        logger.info("tweet content: {}".format(content))
        logger.info("tweet filename: {}".format(filename))

        if len(content) > 140:
            content = content[:140]
            logger.warn("tweet length is excedded: {}".format(len(content)))
            logger.warn("tweet content is trimmed")

        tweet: tweepy.models.Status = self.api.update_status_with_media(
            content, filename
        )
        logger.info("tweet posted successfully")
        logger.info("tweet id: {}".format(tweet.id))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import logging
import os

import tweepy

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

        media: tweepy.models.Media = self.api.media_upload(filename)
        media_id = media.media_id_string
        logging.info("uploaded media, id: {}".format(media_id))

        tweet: tweepy.models.Status = self.api.update_status(
            content, media_ids=[media_id]
        )
        logger.info("tweet posted successfully")
        logger.info("tweet id: {}".format(tweet.id))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import json
import os

import tweepy
from tweepy.tweet import Tweet

from logger import logger


class TwitterCredentials:
    def __init__(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

        self.__verify_authentication()

    def __verify_authentication(self):
        try:
            self.api.verify_credentials()
            logger.info("Twitter api authenticated")
        except tweepy.errors.Unauthorized as e:
            logger.critical("Twitter authentication failed")
            logger.critical("error msg: {}".format(e))
            exit(1)

    @staticmethod
    def read_from_json_file(filename):
        try:
            assert filename and len(filename)

            with open(filename) as f:
                creds = json.load(f)

                assert creds["twitter"]["consumer_key"]
                assert creds["twitter"]["consumer_secret"]
                assert creds["twitter"]["access_token"]
                assert creds["twitter"]["access_token_secret"]

                return TwitterCredentials(
                    creds["twitter"]["consumer_key"],
                    creds["twitter"]["consumer_secret"],
                    creds["twitter"]["access_token"],
                    creds["twitter"]["access_token_secret"],
                )
        except AssertionError as e:
            logger.critical(e)
            exit(1)


class TwitterBot:

    hashtags = "\n#woooosh #reddit #memes"
    tweet_limit = 140

    def __init__(self, credentials: TwitterCredentials):
        self.credentails = credentials
        self.api = self.credentails.api

    def tweet(self, content: str, filename: str):
        logger.info("started posting tweet")
        try:
            self.__validate_content(content)
            self.__validate_filename(filename)

            content = self.__trim_tweet(content)

            media_id = self.__upload_media(filename)
            tweet_id = self.__upload_tweet_with_media(content, media_id)
            logger.info(
                "Tweet posted successfully, tweet id: {}".format(tweet_id)
            )
        except AssertionError as e:
            logger.error("Failed to validate tweet, {}".format(e))
        except tweepy.TwitterServerError as e:
            logger.error("Failed to post tweet, {}".format(e))

    def __trim_tweet(self, content: str) -> str:
        """Trim tweet if too long and add hashtag

        Args:
            content (str): tweet content

        Returns:
            str: trimmed tweet
        """

        if len(content) > self.tweet_limit - len(self.hashtags):
            logger.warning("Tweet content is trimmed")
            content = content[: 140 - len(self.hashtags)]

        return content + self.hashtags

    def __validate_content(self, content):
        assert content and len(content)
        logger.debug("tweet content: {}".format(content))

        if len(content) > self.tweet_limit - len(self.hashtags):
            logger.warning(
                "tweet is too long ({} characters)".format(len(content))
            )

    def __validate_filename(self, filename: str):
        assert filename and len(filename)
        assert os.path.exists(filename)
        logger.debug("Tweet filename: {}".format(filename))

    def __upload_media(self, filename: str) -> int:
        """upload media to twitter

        Args:
            filename (str): filename to upload

        Returns:
            int: media_id
        """
        media: tweepy.models.Media = self.api.media_upload(filename)
        logger.debug(
            "Media uploaded successfully, media id: {}".format(media.media_id)
        )

        return media.media_id

    def __upload_tweet_with_media(self, content: str, media_id: str) -> str:
        """upload tweet content

        Args:
            content (str): tweet content
            media_id (str): uploaded media id

        Returns:
            str: tweet id
        """
        tweet: tweepy.models.Status = self.api.update_status(
            content, media_ids=[media_id]
        )

        logger.debug(
            "Tweet content uploaded successfully, tweet id: {}".format(
                tweet.id
            )
        )

        return tweet.id

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import os

import tweepy

import logger


class TwitterCredentials:
    def __init__(self, key, secret, token, token_secret):
        self.auth = tweepy.OAuthHandler(key, secret)
        self.auth.set_access_token(token, token_secret)
        self.api = tweepy.API(self.auth)

    def verify_credentials(self):
        try:
            self.api.verify_credentials()
            logger.logger.info("Twitter credentials are valid")
        except tweepy.errors.Unauthorized as e:
            logger.logger.fatal(f"Twitter credentials are invalid: {e}")
            exit(1)


class Twitter:
    tweet_limit = 140

    def __init__(self, credentials: TwitterCredentials, hashtags):
        self.credentials = credentials
        self.api = self.credentials.api
        self.hashtags = "\n" + " ".join(hashtags)

    def tweet(self, content: str, filename: str):
        try:
            # validate
            assert content and len(content) > 0
            assert os.path.exists(filename)

            content = content[: self.tweet_limit - len(self.hashtags) - 1]  # 1 for space between content and hashtags
            content += ' ' + self.hashtags

            # Tweet
            media: tweepy.models.Media = self.api.media_upload(filename)
            tweet: tweepy.models.Status = self.api.update_status(content, media_ids=[media.media_id])

            return tweet.id
        except AssertionError as e:
            logger.logger.error(f"Failed to validate tweet, content: {content}, filename: {filename}")
        except tweepy.TwitterServerError as e:
            logger.logger.error(f"Failed to tweet: {e}")
        except tweepy.errors.BadRequest as e:
            logger.logger.error(f"Failed to tweet: {e}")

        return None

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

from config import config
import os
import requests
import shutil
from typing import Deque, List

import praw

from logger import logger


class RedditCredentials:
    def __init__(self, client_id, client_secret):
        self.api = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion",
        )

        self.__verify_auth()

    def __verify_auth(self):
        try:
            self.api.subreddit("woooosh").hot(limit=1)
            logger.info("Reddit api authenticated")
        except Exception as e:
            logger.critical("Reddit authentication failed")
            logger.critical("error msg: {}".format(e))
            exit(1)

    @staticmethod
    def read_from_config():
        try:
            assert config["credentials"]["reddit"]["client_id"]
            assert config["credentials"]["reddit"]["client_secret"]

            return RedditCredentials(
                config["credentials"]["reddit"]["client_id"],
                config["credentials"]["reddit"]["client_secret"],
            )
        except AssertionError as e:
            logger.critical(e)
            exit(1)


class RedditPost:
    def __init__(self, identifier, content, url):
        assert identifier and len(identifier)
        assert content and len(content)
        assert url and len(url)

        self.id = identifier
        self.content = content
        self.url = url
        self.filename = None

    def download_media(self) -> str:
        if self.filename and not os.path.exists(self.filename):
            return self.filename

        logger.info("Started download media from {}".format(self.url))

        r = requests.get(self.url, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True

            filename = os.path.join("/tmp", self.url.split("/")[-1])
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
                self.filename = filename
                logger.debug("Downloaded: {}".format(filename))

        else:
            logger.error(
                "download failed with http status code: {}".format(
                    r.status_code
                )
            )

        return self.filename

    def remove_media(self):
        if self.filename and os.path.exists(self.filename):
            os.remove(self.filename)


class SubredditScrapper:
    def __init__(self, credentails: RedditCredentials):
        self.credentials = credentails
        self.api = self.credentials.api

    def fetch_posts(
        self, subreddit: str = "woooosh", limit: int = 100
    ) -> List[RedditPost]:

        try:
            logger.info(
                "Started fetching {} posts from r/{}".format(limit, subreddit)
            )

            posts: List[RedditPost] = self.__fetch_posts(subreddit, limit)
            logger.info("Fetched {} posts".format(len(posts)))

            posts_with_media: List[
                RedditPost
            ] = self.__filter_posts_with_media(posts)
            logger.info(
                "Filterd {} posts with media".format(len(posts_with_media))
            )

            return posts_with_media
        except AssertionError as e:
            logger.error(e)
        except praw.exceptions.PRAWException as e:
            logger.error("Failed to get posts from subreddit, {}".format(e))

        return []

    def __fetch_posts(self, subreddit: str, limit: int) -> List[RedditPost]:
        assert subreddit and len(subreddit)
        assert limit and 0 < limit <= 100

        res = self.api.subreddit(subreddit).hot(limit=limit)
        res = map(lambda p: RedditPost(p.id, p.title, p.url), res)
        return list(res)

    def __filter_posts_with_media(
        self, posts: List[RedditPost]
    ) -> List[RedditPost]:
        assert posts and len(posts)

        res = filter(lambda p: p.url.endswith(".jpg"), posts)
        return list(res)

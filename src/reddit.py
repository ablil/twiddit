#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import os
import shutil
from typing import List

import praw
import requests

import logger


class RedditCredentials:
    def __init__(self, client_id, client_secret):
        self.api = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion",
        )

    def verify_credentials(self):
        try:
            # todo: check official docs for the api
            self.api.subreddit("woooosh").hot(limit=1)
            logger.logger.info("Reddit credentials are valid")
        except Exception as e:
            logger.logger.fatal(f"Reddit credentials are invalid: {e}")
            exit(1)

    def get_api(self):
        return self.api


class RedditPost:
    def __init__(self, identifier, content, url):
        self.id = identifier
        self.content = content
        self.url = url
        self.filename = None

    def download_media(self) -> str:
        if self.filename and not os.path.exists(self.filename):
            return self.filename

        logger.logger.debug(f"Downloading {self.url}")

        r = requests.get(self.url, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True
            # todo: use temp directory
            filename = os.path.join("/tmp", self.url.split("/")[-1])
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
                self.filename = filename
                logger.logger.debug(f"Downloaded: {filename}")
        else:
            logger.logger.error(f"Download failed, status code: {r.status_code}, url: {self.url}")

        return self.filename

    def remove_media(self):
        if self.filename and os.path.exists(self.filename):
            os.remove(self.filename)


class Reddit:
    def __init__(self, credentials: RedditCredentials):
        self.credentials = credentials
        self.api = self.credentials.get_api()

    def fetch_posts(self, subreddit: str, limit: int, only_media=True) -> List[RedditPost]:
        logger.logger.debug(f"Fetching up to {limit} posts from {subreddit}")

        res = self.api.subreddit(subreddit).hot(limit=limit)
        res = map(lambda p: RedditPost(p.id, p.title, p.url), res)

        if only_media:
            logger.logger.debug(f"Filtering only media posts ...")
            res = list(filter(lambda p: p.url.endswith(".jpg") or p.url.endswith('.png'), res))

        logger.logger.info(f"Total fetched posts {len(res)}")
        return list(res)

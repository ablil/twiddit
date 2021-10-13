#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import logging
from typing import Deque, List

import praw

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SubredditScrapper:
    subreddit = "woooosh"
    posts_limit = 100

    def __init__(self, client_id, client_secret):
        self.api = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion",
        )
        logger.info("connected to reddit api")

    def fetch_hot_posts(self, queue: List):
        """extend the given queue with the latest hostest posts from subreddit

        Args:
            queue (Deque): queue (FIFO) to extend
        """
        logger.info("started fetching hottest reddit posts")

        posts = list(
            self.api.subreddit(SubredditScrapper.subreddit).hot(
                limit=SubredditScrapper.posts_limit
            )
        )
        logger.info(
            "fetched {} posts from subreddit {}".format(
                len(posts), SubredditScrapper.subreddit
            )
        )

        posts_with_media = list(filter(lambda p: p.url.endswith(".jpg"), posts))
        logger.info("filterd only {} posts with media".format(len(posts_with_media)))

        counter = 0
        for post in posts_with_media:
            if post.url.endswith(".jpg"):
                queue.append((post.id, post.title, post.url))
                counter += 1

        logging.info("added {} new posts from reddit".format(counter))

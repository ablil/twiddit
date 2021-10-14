#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

from typing import Deque, List

import praw

from logger import logger


class SubredditScrapper:
    subreddit = "woooosh"
    posts_limit = 100

    def __init__(self, client_id, client_secret):
        self.api = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion",
        )

        self.__verify_auth()

    def run(self, queue: List):
        """extend the given queue with the latest hostest posts from subreddit

        Args:
            queue (Deque): queue (FIFO) to extend
        """
        logger.info("started fetching hottest reddit posts")

        try:
            posts_with_media = self.__fetch_posts_with_media(queue)
            counter = 0
            for post in posts_with_media:
                if post.url.endswith(".jpg"):
                    queue.append((post.id, post.title, post.url))
                    counter += 1

            logger.info("added {} new posts from reddit".format(counter))

        except Exception as e:
            logger.error("Failed to get reddit posts")
            logger.error(e)

    def __fetch_posts_with_media(self, queue):
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

        return posts_with_media

    def __verify_auth(self):
        try:
            self.__fetch_posts_with_media(queue=[])
            logger.info("Reddit api authenticated")
        except Exception as e:
            logger.critical("Reddit authentication failed")
            logger.critical("error msg: {}".format(e))
            exit(1)

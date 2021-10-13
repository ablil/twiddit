#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

from os import posix_fadvise
import praw
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RedditParser:
    def __init__(self, client_id, client_secret):
        self.api = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion",
        )
        logger.info("connected to reddit api")

    def fetch_hot_posts(self):
        logger.info("started fetching hottest reddit posts")

        posts = list(self.api.subreddit("woooosh").hot())
        logger.info("fetched {} posts from reddits".format(len(posts)))

        posts_with_media = list(filter(lambda post: post.url.endswith(".jpg"), posts))
        logger.info("filterd only {} posts with media".format(len(posts_with_media)))
        for post in self.api.subreddit("woooosh").hot():
            if post.url.endswith(".jpg"):
                posts.append((post.id, post.title, post.url))

        return list(map(lambda p: (p.id, p.title, p.url), posts_with_media))

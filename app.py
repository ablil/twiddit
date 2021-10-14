#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import collections
import json
import os
import shutil
import time

import requests

import reddit
import twitter
from logger import logger


def get_credentials():
    if not os.path.exists("./credentials.json"):
        logger.critical("credentials.json file not found")
        exit(1)

    with open("./credentials.json") as f:
        return json.load(f)


def download_picture(url: str) -> str:
    """download picture and return filename"""
    logger.info("started downloading image from url: {}".format(url))
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        filename = os.path.join("/tmp", url.split("/")[-1])
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)

        logger.info("downloaded picture: {}".format(filename))
        return filename
    else:
        logger.error("download failed with http status code: {}".format(r.status_code))

    return None


def main():
    print("Running ...")
    logger.info("Starting ...")
    credentials = get_credentials()
    posts = []

    twitter_bot = twitter.Bot(
        credentials["twitter"]["key"],
        credentials["twitter"]["key_secret"],
        credentials["twitter"]["token"],
        credentials["twitter"]["token_secret"],
    )
    reddit_scrapper = reddit.SubredditScrapper(
        credentials["reddit"]["client_id"], credentials["reddit"]["secret"]
    )

    failure = 0

    while True:
        reddit_scrapper.run(posts)

        if not len(posts):
            failure += 1
            logger.info(
                "No post is available, waiting for 60 min before fetching again"
            )
            time.sleep(60 * 60)  # wait for 60 min until new posts are available

        if failure >= 10:
            logger.critical(
                "Attempted to get reddit posts {} times, and got no response".format(
                    failure
                )
            )
            exit(1)

        while len(posts):
            post_id, post_content, post_image = posts.pop(0)
            image_filename = download_picture(post_image)
            if image_filename:
                twitter_bot.run(post_content, image_filename)

                os.remove(image_filename)
                logger.info("removed {}".format(image_filename))

            time.sleep(60 * 15)


if __name__ == "__main__":
    main()

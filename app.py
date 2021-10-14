#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import collections
import json
import logging
import os
import shutil
import time

import requests

import reddit
import twitter


def configure_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logfile = os.path.join("logs", time.strftime("%Y-%m-%d-%H-%M") + ".log")
    logging.basicConfig(filename=logfile, filemode="a+", level=logging.INFO)


def get_credentials():
    if not os.path.exists("./credentials.json"):
        logging.critical("credentials.json file not found")
        exit(1)

    with open("./credentials.json") as f:
        return json.load(f)


def download_picture(url: str) -> str:
    """download picture and return filename"""
    logging.info("started downloading image from url: {}".format(url))
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        filename = os.path.join("/tmp", url.split("/")[-1])
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)

        logging.info("downloaded picture: {}".format(filename))
        return filename
    else:
        logging.error("download failed with http status code: {}".format(r.status_code))

    return None


def main():
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

        if failure >= 10:
            logging.critical("Attempted to get reddit posts {} times, and got no response".format(failure))
            exit(1)

        while len(posts):
            post_id, post_content, post_image = posts.pop(0)
            image_filename = download_picture(post_image)
            if image_filename:
                twitter_bot.run(post_content, image_filename)

                os.remove(image_filename)
                logging.info("removed {}".format(image_filename))

            time.sleep(60)  # sleep for 30 min before posting again


if __name__ == "__main__":
    configure_logging()
    main()

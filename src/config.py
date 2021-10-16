#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-16

from dotenv import load_dotenv
import os
from logger import logger

env_config = load_dotenv()

# default config
config = {
    "credentials": {
        "twitter": {
            "consumer_key": None,
            "consumer_secret": None,
            "access_token": None,
            "access_token_secret": None,
        },
        "reddit": {
            "client_id": None,
            "client_secret": None,
        },
    },
    "bot": {
        "subreddit": "woooosh",
        "hashtags": ["#woooosh", "#reddit", "#memes"],
        "time_to_post": 60 * 15,
    },
    "branding": {
        "time_to_like": 60,
        "hashtags": ["#reddit", "#memes"],
    },
}

# load from .env
try:
    config["credentials"]["twitter"]["consumer_key"] = os.environ[
        "twitter_consumer_key"
    ]
    config["credentials"]["twitter"]["consumer_secret"] = os.environ[
        "twitter_consumer_secret"
    ]
    config["credentials"]["twitter"]["access_token"] = os.environ[
        "twitter_access_token"
    ]
    config["credentials"]["twitter"]["access_token_secret"] = os.environ[
        "twitter_access_token_secret"
    ]

    config["credentials"]["reddit"]["client_id"] = os.environ[
        "reddit_client_id"
    ]
    config["credentials"]["reddit"]["client_secret"] = os.environ[
        "reddit_client_secret"
    ]
except KeyError as e:
    logger.critical(e)


bot_subreddit = os.environ.get("bot_subreddit")
if bot_subreddit and len(bot_subreddit):
    config["bot"]["subreddit"] = bot_subreddit

bot_hashtags = os.environ.get("bot_hashtags")
if bot_hashtags and len(bot_hashtags):
    config["bot"]["hashtags"] = list(
        map(lambda h: "#" + h, bot_hashtags.split(","))
    )

bot_time_to_post = os.environ.get("bot_time_to_post")
if bot_time_to_post and len(bot_time_to_post):
    try:
        bot_time_to_post = int(bot_time_to_post)
        assert bot_time_to_post > 0
        config["bot"]["time_to_post"]
    except AssertionError:
        logger.warning(
            "bot_time_to_post is not a positive value, defaulting to 900 seconds"
        )
    except ValueError:
        logger.warn(
            "bot_time_to_post value is not an integer, defaulting to 900"
        )

branding_time_to_like = os.environ.get("branding_time_to_like")
if branding_time_to_like and len(branding_time_to_like):
    try:
        branding_time_to_like = int(branding_time_to_like)
        assert branding_time_to_like > 0
        config["branding"]["time_to_like"] = branding_time_to_like
    except AssertionError:
        logger.warning(
            "branding_time_to_like is not a positive value, defaulting to 60 seconds"
        )
    except ValueError:
        logger.warn(
            "branding_time_to_like value is not an integer, defaulting to 60"
        )

branding_hashtags = os.environ.get("branding_hashtags")
if branding_hashtags and len(branding_hashtags):
    config["branding"]["hashtags"] = list(
        map(lambda h: "#" + h, branding_hashtags.split(","))
    )

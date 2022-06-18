#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-16
import logging

import dotenv
from logger import logger


def validate_config_existence(key: str, config: dict):
    if key not in config.keys():
        logger.fatal(f"Property {key} is missing !!!")
        exit(1)


def validate_int_property(key, value):
    try:
        assert int(value) > 0
    except AssertionError:
        logger.fatal(f"Property {key} should be a positive value")
        exit(1)
    except ValueError:
        logger.fatal(f"Property {key} should be a number")
        exit(1)


def validate_config_value(key, value):
    if not (value and len(value) > 0):
        logger.fatal(f"{key} is empty !!!")
        exit(1)


def load_config(path):
    config = dotenv.dotenv_values(path)

    # check if all properties exist
    validate_config_existence('reddit_client_id', config)
    validate_config_existence('reddit_client_secret', config)

    validate_config_existence('twitter_consumer_key', config)
    validate_config_existence('twitter_consumer_secret', config)
    validate_config_existence('twitter_access_token', config)
    validate_config_existence('twitter_access_token_secret', config)

    validate_config_existence('bot_subreddit', config)
    validate_config_existence('bot_frequency', config)
    validate_config_existence('bot_hashtags', config)
    validate_config_existence('bot_posts_limit', config)

    # check if a property is empty
    for key in config:
        validate_config_value(key, config[key])

    # validate custom properties
    validate_int_property('bot_frequency', config['bot_frequency'])
    validate_int_property('bot_posts_limit', config['bot_posts_limit'])

    return config

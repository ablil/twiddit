#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-13

import time
from typing import List

import config
import logger
from reddit import Reddit, RedditCredentials, RedditPost
from twitter import Twitter, TwitterCredentials

posted = []


def main():
    bot_config = config.load_config('.env')

    reddit_credentials: RedditCredentials = RedditCredentials(bot_config['reddit_client_id'],
                                                              bot_config['reddit_client_secret'])
    reddit_credentials.verify_credentials()

    twitter_credentials: TwitterCredentials = TwitterCredentials(bot_config['twitter_consumer_key'],
                                                                 bot_config['twitter_consumer_secret'],
                                                                 bot_config['twitter_access_token'],
                                                                 bot_config['twitter_access_token_secret'])
    twitter_credentials.verify_credentials()

    hashtags = [hashtag.strip() for hashtag in bot_config['bot_hashtags'].split(',')]
    if len(hashtags):
        hashtags = ['#' + hashtag for hashtag in hashtags]

    reddit_client: Reddit = Reddit(reddit_credentials)
    twitter_client: Twitter = Twitter(twitter_credentials, hashtags)

    while True:
        reddit_posts: List[RedditPost] = reddit_client.fetch_posts(bot_config['bot_subreddit'],
                                                                   int(bot_config['bot_posts_limit']))
        for post in reddit_posts:
            if post.id not in posted:
                downloaded_media: str = post.download_media()
                tweet_id: str = twitter_client.tweet(post.content, downloaded_media)
                logger.logger.info(f"Posted tweet: {tweet_id}")

                posted.append(post.id)
                time.sleep(60 * int(bot_config['bot_frequency']))
            else:
                logger.logger.warn(f"Reddit post {post.id} is already posted")

        if len(posted) > 100:
            posted.clear()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

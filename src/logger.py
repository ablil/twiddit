#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ablil <ablil@protonmail.com>
# created: 2021-10-14

import logging
import os
import time

import coloredlogs

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger(__name__)

logfile = os.path.join("logs", time.strftime("%Y-%m-%d-%H-%M") + ".log")
loglevel = logging.INFO  # fixme: check appropriate log leve

# log to file
file = logging.FileHandler(logfile, mode="a+")
file.setLevel(loglevel)
file.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(file)

# log to stdout
stream = logging.StreamHandler()
stream.setLevel(loglevel)
stream.setFormatter(
    logging.Formatter(
        "%(asctime)s %(module)s %(funcName)s %(levelname)s %(message)s"
    )
)
logger.addHandler(stream)

coloredlogs.install(
    level=loglevel,
    logger=logger,
    fmt="%(asctime)s:%(levelname)s:%(module)s - %(message)s",
)

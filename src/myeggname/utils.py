#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys


def configure_logging(app_logger_name: str, verbosity: int = 0,
                      default_level: int = logging.WARN) -> logging.Logger:
    """
    Configure Python logging for the application.

    :param app_logger_name: The logger name for the application, e.g. 'myapp'.
    :param verbosity: The verbosity to modify the logger level with. Passing 0
                      will leave the level at `default_level`. Any positive
                      integer will increase the level _n_ times, where _n_ is
                      the value of `verbosity`.
    :param default_level: The default logging level for the application, to be
                          modified by the `verbosity` parameter.
    :return: Returns the app logger with the given name after logging has been
             configured.
    """

    # rename the warning level to simply 'warn'
    logging.addLevelName(logging.WARNING, "WARN")

    # create a formatter
    formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)-5s] "
                                      "%(name)s: %(message)s",
                                  datefmt="%Y-%m-%dT%H:%M:%S")

    # setup the handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)

    # register the handler
    logging.root.addHandler(handler)

    # create the app logger
    logger = logging.getLogger(app_logger_name)
    # set the logger level by using the default level and increasing verbosity
    # by one level for each value in verbosity; passing 0 here means that we
    # don't increase verbosity, passing 1 means we increase verbosity by one
    # level, passing 2 means we increase verbosity by two levels, etc.
    logger.setLevel(max(default_level - (verbosity * 10), logging.DEBUG))

    return logger


async def yield_now():
    """
    Immediately yield the event loop back to the executor to potentially allow
    other coroutines to run.
    """
    return asyncio.sleep(0)

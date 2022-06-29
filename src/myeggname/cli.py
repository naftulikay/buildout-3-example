#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging

from .utils import configure_logging


def run_argparse():
    parser = argparse.ArgumentParser(description="Example script in argparse.")
    parser.add_argument('-v', action='count', default=0, dest='verbosity',
                        help="Increase logging verbosity, pass multiple times "
                             "to increase verbosity further.")
    args = parser.parse_args()

    logger = configure_logging('myeggname', verbosity=args.verbosity,
                               default_level=logging.WARNING)

    logger.debug("Hello Debug")
    logger.info("Hello Info")
    logger.warning("Hello Warn")
    logger.error("Hello Error")


def run_click():
    pass

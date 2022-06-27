#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple

import unittest


class OldFashionedTest(unittest.TestCase):

    def test_one(self):
        self.assertTrue(True, msg="True was not true.")

    def test_two(self):
        self.assertEqual(4, 2 + 2, msg="2+2 was not 4.")

    def test_duration_calculator(self):
        def duration_dhms(secs: int) -> Tuple[int, int, int, int]:
            days, hours, minutes, seconds = 0, 0, 0, 0

            if secs > 0:
                days, rem = divmod(secs, 24 * 60 * 60)

                if rem > 0:
                    hours, rem = divmod(rem, 60 * 60)

                if rem > 0:
                    minutes, seconds = divmod(rem, 60)

            return days, hours, minutes, seconds

        MINUTE_SECS = (60)
        HOUR_SECS = (60 * MINUTE_SECS)
        DAY_SECS = (24 * HOUR_SECS)

        # 23 hours
        self.assertEqual((0, 23, 0, 0), duration_dhms(23 * HOUR_SECS))
        # 1 day
        self.assertEqual((1, 0, 0, 0), duration_dhms(1 * DAY_SECS))
        # 1 day and 1 hour
        self.assertEqual((1, 1, 0, 0),
                         duration_dhms((1 * DAY_SECS) + (1 * HOUR_SECS)))
        # 1 day, 1 hour, 1 minute
        self.assertEqual((1, 1, 1, 0),
                         duration_dhms((1 * DAY_SECS) + (1 * HOUR_SECS) +
                                       (1 * MINUTE_SECS)))
        # 1 day, 1 hour, 1 minute, 1 second
        self.assertEqual((1, 1, 1, 1),
                         duration_dhms((1 * DAY_SECS) + (1 * HOUR_SECS) +
                                       (1 * MINUTE_SECS) + 1))


def test_nose_way():
    assert 2+2 == 4

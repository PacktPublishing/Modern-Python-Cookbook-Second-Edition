"""Python Cookbook 2nd ed.

Chapter 11, recipe 4 and 5. Unittest and Doctest.
"""

from Chapter_11.ch11_r01 import Summary

import unittest
import random


class GIVEN_data_WHEN_1k_samples_THEN_mean_median(unittest.TestCase):
    def setUp(self):
        self.summary = Summary()
        self.data = list(range(1001))
        random.shuffle(self.data)

    def runTest(self):
        for sample in self.data:
            self.summary.add(sample)

        self.assertEqual(500, self.summary.mean)
        self.assertEqual(500, self.summary.median)


class GIVEN_Summary_WHEN_1k_samples_THEN_mean_median(unittest.TestCase):
    def setUp(self):
        self.summary = Summary()
        self.data = list(range(1001))
        random.shuffle(self.data)
        for sample in self.data:
            self.summary.add(sample)

    def test_mean(self):
        self.assertEqual(500, self.summary.mean)

    def test_median(self):
        self.assertEqual(500, self.summary.median)


class GIVEN_Summary_WHEN_1k_samples_THEN_mode(unittest.TestCase):
    def setUp(self):
        self.summary = Summary()
        self.data = [500] * 97
        # Build 903 elements: each value of n occurs n times.
        for i in range(1, 43):
            self.data += [i] * i
        random.shuffle(self.data)
        for sample in self.data:
            self.summary.add(sample)

    def test_mode(self):
        top_3 = self.summary.mode[:3]
        self.assertListEqual([(500, 97), (42, 42), (41, 41)], top_3)


# Recipe 5 -- combining. Requires unittest.

import Chapter_11.ch11_r01


def load_tests(loader, standard_tests, pattern):
    import doctest

    dt = doctest.DocTestSuite(Chapter_11.ch11_r01)
    standard_tests.addTests(dt)
    return standard_tests

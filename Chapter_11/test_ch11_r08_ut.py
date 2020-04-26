"""Python Cookbook 2nd ed.

Chapter 11, recipe 8. Testing things that involve dates or times
Unittest Variant.
"""
import datetime
import json
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
import Chapter_11.ch11_r08


class GIVEN_data_WHEN_save_data_THEN_file(unittest.TestCase):
    def setUp(self):
        self.data = {"primes": [2, 3, 5, 7, 11, 13, 17, 19]}
        self.mock_datetime = Mock(
            datetime=Mock(
                utcnow=Mock(return_value=datetime.datetime(2017, 7, 4, 1, 2, 3))
            )
        )
        self.expected_name = "extract_20170704010203.json"
        self.expected_path = Path("data") / self.expected_name
        if self.expected_path.exists():
            self.expected_path.unlink()

    def runTest(self):
        with patch("Chapter_11.ch11_r08.datetime", self.mock_datetime):
            Chapter_11.ch11_r08.save_data(Path("data"), self.data)
        with self.expected_path.open() as result_file:
            result_data = json.load(result_file)
        self.assertDictEqual(self.data, result_data)

        self.mock_datetime.datetime.utcnow.assert_called_once_with()
        self.assertFalse(self.mock_datetime.datetime.called)

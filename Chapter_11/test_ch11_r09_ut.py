"""Python Cookbook 2nd ed.

Chapter 11, recipe 9. Testing things that involve randomness
Unittest Variant.
"""

import unittest
from unittest.mock import Mock, patch, call
import Chapter_11.ch11_r09


class GIVEN_resample_WHEN_evaluated_THEN_fair(unittest.TestCase):
    def setUp(self):
        self.data = [2, 3, 5, 7, 11, 13, 17, 19]
        self.expected_resample_data = [23, 29, 31, 37, 41, 43, 47, 53]
        self.mock_random = Mock(choice=Mock(side_effect=self.expected_resample_data))

    def runTest(self):
        with patch("Chapter_11.ch11_r09.random", self.mock_random):
            resample_data = list(Chapter_11.ch11_r09.resample(self.data, 8))

        self.assertListEqual(self.expected_resample_data, resample_data)

        self.mock_random.choice.assert_has_calls(8 * [call(self.data)])

"""Python Cookbook

Chapter 13, recipe 5. Designing scripts for composition
"""
from pathlib import Path
import os
import unittest
import yaml
import Chapter_13.ch13_r05


class GIVEN_ch13_r05_WHEN_run_app_THEN_output(unittest.TestCase):
    def setUp(self):
        self.data_path = Path("data/ch13_r05_test.yaml")
        if self.data_path.exists():
            self.data_path.unlink()

    def runTest(self):
        os.environ["RANDOMSEED"] = "2"
        options = Chapter_13.ch13_r05.get_options(
            ["--samples", "10", "--output", "data/ch13_r05_test.yaml"]
        )
        face_count = Chapter_13.ch13_r05.write_rolls(
            options.output_path,
            Chapter_13.ch13_r05.roll_iter(options.samples, options.seed),
        )
        self.assertDictEqual(
            {8: 8, 7: 6, 10: 5, 4: 3, 6: 3, 9: 3, 2: 2, 3: 1, 5: 1, 11: 1, 12: 1},
            face_count,
        )
        results = list(
            yaml.load_all(self.data_path.read_text(), Loader=yaml.SafeLoader)
        )
        self.assertListEqual(
            [
                [[1, 1]],
                [[1, 3], [2, 6], [6, 3], [3, 5], [2, 5]],
                [
                    [1, 5],
                    [6, 2],
                    [4, 6],
                    [4, 6],
                    [5, 3],
                    [5, 4],
                    [5, 3],
                    [1, 1],
                    [3, 4],
                ],
                [[3, 4]],
                [[4, 5], [2, 5]],
                [[2, 2], [2, 1], [2, 3], [2, 2]],
                [[5, 5], [3, 5], [6, 5], [2, 4], [4, 6]],
                [[5, 3], [5, 3]],
                [[3, 4]],
                [[2, 4], [6, 6], [4, 6], [5, 2]],
            ],
            results,
        )

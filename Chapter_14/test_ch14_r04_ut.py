"""Python Cookbook

Chapter 14, recipe 4, Wrapping and combining CLI applications
"""
from pathlib import Path
import subprocess
import unittest
from unittest.mock import Mock, patch, call
import Chapter_14.ch14_r04


class GIVEN_make_files_WHEN_call_THEN_run(unittest.TestCase):
    def setUp(self):
        self.mock_subprocess_run = Mock()

    def runTest(self):
        with patch("Chapter_14.ch14_r04.subprocess.run", self.mock_subprocess_run):
            Chapter_14.ch14_r04.make_files_clean(Path("data"), files=3)
        self.mock_subprocess_run.assert_has_calls(
            [
                call(
                    [
                        "python",
                        "Chapter_13/ch13_r05.py",
                        "--samples",
                        "10",
                        "--output",
                        "data/game_0.yaml",
                    ],
                    check=True,
                ),
                call(
                    [
                        "python",
                        "Chapter_13/ch13_r05.py",
                        "--samples",
                        "10",
                        "--output",
                        "data/game_1.yaml",
                    ],
                    check=True,
                ),
                call(
                    [
                        "python",
                        "Chapter_13/ch13_r05.py",
                        "--samples",
                        "10",
                        "--output",
                        "data/game_2.yaml",
                    ],
                    check=True,
                ),
            ]
        )


class GIVEN_make_files_exception_WHEN_call_THEN_run(unittest.TestCase):
    def setUp(self):
        self.mock_subprocess_run = Mock(
            side_effect=[None, subprocess.CalledProcessError(2, "ch13_r05")]
        )
        self.mock_path_glob_instance = Mock(
            name="data/file*"
        )
        self.mock_file_path_instance = Mock(
            name="data/file"
        )
        self.mock_base_path_instance = Mock(
            name="data",
            glob=Mock(return_value=[self.mock_path_glob_instance])
        )
        self.mock_base_path_instance.__truediv__ = Mock(
            side_effect=lambda n: f"data/{n}"
        )

    def runTest(self):
        with patch(
            "Chapter_14.ch14_r04.subprocess.run", self.mock_subprocess_run
        ):
            self.assertRaises(
                subprocess.CalledProcessError,
                Chapter_14.ch14_r04.make_files_clean,
                self.mock_base_path_instance,
                files=3
            )
        self.mock_subprocess_run.assert_has_calls(
            [
                call(
                    [
                        "python",
                        "Chapter_13/ch13_r05.py",
                        "--samples",
                        "10",
                        "--output",
                        "data/game_0.yaml",
                    ],
                    check=True,
                ),
                call(
                    [
                        "python",
                        "Chapter_13/ch13_r05.py",
                        "--samples",
                        "10",
                        "--output",
                        "data/game_1.yaml",
                    ],
                    check=True,
                ),
            ]
        )
        self.assertEqual(2, self.mock_subprocess_run.call_count)
        self.mock_base_path_instance.glob.assert_called_once_with("game_*.yaml")
        self.mock_path_glob_instance.unlink.assert_called_once_with()

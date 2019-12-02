"""Python Cookbook

Chapter 13, recipe 10
"""
import unittest
from unittest.mock import Mock, patch, call
import subprocess
import Chapter_13.ch13_r10


class GIVEN_make_files_WHEN_call_THEN_run(unittest.TestCase):
    def setUp(self):
        self.mock_subprocess_run = Mock()

    def runTest(self):
        with patch("Chapter_13.ch13_r10.subprocess.run", self.mock_subprocess_run):
            Chapter_13.ch13_r10.make_files(files=3)
        self.mock_subprocess_run.assert_has_calls(
            [
                call(
                    [
                        "python3",
                        "ch13_r05.py",
                        "--samples",
                        "10",
                        "--output",
                        "data/game_0.yaml",
                    ],
                    check=True,
                ),
                call(
                    [
                        "python3",
                        "ch13_r05.py",
                        "--samples",
                        "10",
                        "--output",
                        "data/game_1.yaml",
                    ],
                    check=True,
                ),
                call(
                    [
                        "python3",
                        "ch13_r05.py",
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
        self.mock_path_glob_instance = Mock()
        self.mock_path_instance = Mock(
            glob=Mock(return_value=[self.mock_path_glob_instance])
        )
        self.mock_path_class = Mock(return_value=self.mock_path_instance)

    def runTest(self):
        with patch(
            "Chapter_13.ch13_r10.subprocess.run", self.mock_subprocess_run
        ), patch("Chapter_13.ch13_r10.Path", self.mock_path_class):
            self.assertRaises(
                subprocess.CalledProcessError, Chapter_13.ch13_r10.make_files, files=3
            )
        self.mock_subprocess_run.assert_has_calls(
            [
                call(
                    [
                        "python3",
                        "ch13_r05.py",
                        "--samples",
                        "10",
                        "--output",
                        "data/game_0.yaml",
                    ],
                    check=True,
                ),
                call(
                    [
                        "python3",
                        "ch13_r05.py",
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
        self.mock_path_class.assert_called_once_with("data")
        self.mock_path_instance.glob.assert_called_once_with("game_*.yaml")
        self.mock_path_glob_instance.unlink.assert_called_once_with()

"""Python Cookbook

Chapter 13, recipe 1.
"""
from pathlib import Path
import unittest
from unittest.mock import Mock, patch, mock_open, MagicMock, call
import Chapter_13.ch13_r01


class GIVEN_get_config_WHEN_load_THEN_overrides_found(unittest.TestCase):
    def setUp(self):
        self.system_exist = Mock(
            name="mock Path('/etc').exist() == True",
            exists=Mock(return_value=True),
            open=mock_open(),
        )
        self.mock_system_path = Mock(
            name='mock Path("/etc")',
            __truediv__=Mock(return_value=self.system_exist),
        )

        self.exist = Mock(
            name="mock Path.home().exist() == True",
            exists=Mock(return_value=True),
            open=mock_open(),
        )
        self.not_exist = Mock(
            name="mock Path.home().exist() == False",
            exists=Mock(return_value=False)
        )
        self.mock_home_path = Mock(
            name="mock Path.home()",
            __truediv__=Mock(side_effect=[self.not_exist, self.exist, self.exist]),
        )

        self.mock_path = Mock(
            name="mock Path class",
            return_value=self.mock_system_path,  # Path("/etc")
            home=Mock(return_value=self.mock_home_path),  # Path.home()
        )
        self.mock_load_config_file = Mock(
            name="mock_load_config_file",
            side_effect=[{"some_setting": 1}, {"another_setting": 2}],
        )

    def runTest(self):
        with patch("Chapter_13.ch13_r01.Path", self.mock_path), patch(
            "Chapter_13.ch13_r01.load_config_file", self.mock_load_config_file
        ):
            config = Chapter_13.ch13_r01.get_config()
        # print(config)
        self.assertEqual(2, config["another_setting"])
        self.assertEqual(1, config["some_setting"])
        self.assertEqual("Built-In Choice", config["some_option"])

        # print(self.mock_load.mock_calls)
        self.mock_load_config_file.assert_has_calls(
            [call(self.system_exist), call(self.exist)]
        )

        # print(self.mock_expanded_home_path.mock_calls)
        self.mock_home_path.assert_has_calls(
            [
                call.__truediv__(".bash_profile"),
                call.__truediv__(".bash_login"),
                call.__truediv__(".profile"),
            ]
        )

        # print(self.mock_path.mock_calls)
        self.mock_path.assert_has_calls(
            [call("/etc"), call.home(), call.home(), call.home()]
        )

        self.exist.assert_has_calls([call.exists()])
        self.system_exist.assert_has_calls([call.exists()])


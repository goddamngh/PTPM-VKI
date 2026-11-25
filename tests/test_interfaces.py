import unittest
from unittest.mock import patch
from src.interfaces import ConsoleInteraction, EmailServerDependency


class TestConsoleInteraction(unittest.TestCase):

    @patch("builtins.input", return_value="42")
    def test_get_input_returns_string(self, mock_input):
        ui = ConsoleInteraction()
        result = ui.get_input("prompt: ")
        self.assertEqual(result, "42")
        mock_input.assert_called_once_with("prompt: ")

    @patch("builtins.print")
    def test_show_output_calls_print(self, mock_print):
        ui = ConsoleInteraction()
        ui.show_output("hello")
        mock_print.assert_called_once_with("hello")


class TestEmailServerDependency(unittest.TestCase):

    def test_send_data_returns_true(self):
        ext = EmailServerDependency()
        result = ext.send_data("test payload")
        self.assertTrue(result)

    @patch("builtins.print")
    def test_send_data_prints_imitation(self, mock_print):
        ext = EmailServerDependency()
        ext.send_data("data")
        mock_print.assert_called_once()


if __name__ == "__main__":
    unittest.main()
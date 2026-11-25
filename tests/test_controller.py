import unittest
from unittest.mock import Mock, patch
from src.controller import Controller


class TestControllerIntegration(unittest.TestCase):
    """Интеграционные тесты контроллера с тестовыми заглушками."""

    def setUp(self):
        self.mock_ui = Mock()
        self.mock_db = Mock()
        self.mock_ext = Mock()
        self.controller = Controller(self.mock_ui, self.mock_db, self.mock_ext)

    def test_new_triangle_not_in_db_computed_and_sent(self):
        """Интеграционный тест: треугольник не в БД — вычисляется, сохраняется и отправляется."""
        self.mock_ui.get_input.side_effect = ["3", "4", "5"]
        self.mock_db.get_record.return_value = None
        self.mock_ext.send_data.return_value = True

        result = self.controller.process_triangle()

        self.mock_db.add_record.assert_called_once()
        self.mock_ext.send_data.assert_called_once_with("Тип: разносторонний")
        self.assertIn("разносторонний", result)

    def test_triangle_found_in_db_cache_used(self):
        """Интеграционный тест: треугольник в БД — берётся из кэша, вычисление не вызывается."""
        self.mock_ui.get_input.side_effect = ["5", "5", "5"]
        self.mock_db.get_record.return_value = ("равносторонний", "")
        self.mock_ext.send_data.return_value = True

        result = self.controller.process_triangle()

        self.mock_db.add_record.assert_not_called()
        self.mock_ext.send_data.assert_called_once_with("Тип: равносторонний")
        self.assertIn("равносторонний", result)

    def test_invalid_string_input_handled(self):
        """Интеграционный тест: нечисловой ввод — корректно обрабатывается."""
        self.mock_ui.get_input.side_effect = ["abc", "4", "5"]
        self.mock_db.get_record.return_value = None
        self.mock_ext.send_data.return_value = True

        result = self.controller.process_triangle()

        self.mock_ext.send_data.assert_called_once()
        self.assertIn("нечисловые", result)

    def test_not_a_triangle_sent_to_external(self):
        """Интеграционный тест: нарушено неравенство треугольника — отправляется результат."""
        self.mock_ui.get_input.side_effect = ["1", "2", "10"]
        self.mock_db.get_record.return_value = None
        self.mock_ext.send_data.return_value = True

        result = self.controller.process_triangle()

        self.mock_db.add_record.assert_called_once()
        self.mock_ext.send_data.assert_called_once()
        self.assertIn("не треугольник", result)

    @patch("src.controller.get_triangle_type_and_coords")
    def test_external_dependency_failure_logged(self, mock_calc):
        """Интеграционный тест: внешняя зависимость возвращает False — результат всё равно возвращается."""
        self.mock_ui.get_input.side_effect = ["3", "4", "5"]
        self.mock_db.get_record.return_value = None
        self.mock_ext.send_data.return_value = False
        mock_calc.return_value = ("разносторонний", [(10, 90), (50, 90), (30, 50)])

        result = self.controller.process_triangle()

        self.mock_ext.send_data.assert_called_once()
        self.assertIn("разносторонний", result)


if __name__ == "__main__":
    unittest.main()
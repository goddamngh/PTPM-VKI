import unittest
from src.triangle import get_triangle_type_and_coords

class TestTriangleApp(unittest.TestCase):

    def test_equilateral_triangle(self):
        """1. Тест равностороннего треугольника"""
        t_type, coords = get_triangle_type_and_coords("5", "5", "5")
        self.assertEqual(t_type, "равносторонний")
        self.assertNotEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_isosceles_triangle(self):
        """2. Тест равнобедренного треугольника"""
        t_type, _ = get_triangle_type_and_coords("4", "4", "5")
        self.assertEqual(t_type, "равнобедренный")

    def test_scalene_triangle(self):
        """3. Тест разностороннего треугольника"""
        t_type, _ = get_triangle_type_and_coords("3", "4", "5")
        self.assertEqual(t_type, "разносторонний")

    def test_floating_point_precision(self):
        """4. Тест на точность float"""
        t_type, coords = get_triangle_type_and_coords("0.1", "0.2", "0.3")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])


    def test_not_a_triangle_inequality(self):
        """5. Нарушено неравенство треугольника (одна сторона слишком большая)"""
        t_type, _ = get_triangle_type_and_coords("1", "2", "10")
        self.assertEqual(t_type, "не треугольник")

    def test_zero_sides(self):
        """6. Одна из сторон равна нулю"""
        t_type, coords = get_triangle_type_and_coords("0", "5", "5")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_sides(self):
        """7. Присутствуют отрицательные стороны"""
        t_type, _ = get_triangle_type_and_coords("-3", "4", "5")
        self.assertEqual(t_type, "не треугольник")

    def test_string_input_error(self):
        """8. Переданы буквы вместо чисел"""
        t_type, coords = get_triangle_type_and_coords("abc", "4", "5")
        self.assertEqual(t_type, "") 
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_empty_input_error(self):
        """9. Переданы пустые строки"""
        t_type, coords = get_triangle_type_and_coords("", "", "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_spaces_in_input(self):
        """10. Числа с пробелами (float должен их успешно обработать)"""
        t_type, _ = get_triangle_type_and_coords("  5.0 ", " 5.0", "5.0  ")
        self.assertEqual(t_type, "равносторонний")

if __name__ == "__main__":
    unittest.main()

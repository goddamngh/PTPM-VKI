import unittest
from src.Delivery import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):

    def test_basic_ordinary_delivery(self):
        """1. Обычная доставка без надбавок"""
        cost, date = calculate_delivery_cost(2.0, 1000, "обычный")
        self.assertEqual(cost, 5200)
        self.assertEqual(date, "2026-09-05")

    def test_weight_surcharge_medium(self):
        """2. Надбавка за вес 5-20 кг (×1.2)"""
        cost, _ = calculate_delivery_cost(10.0, 1000, "обычный")
        self.assertEqual(cost, 6240)

    def test_weight_surcharge_heavy(self):
        """3. Надбавка за вес >=20 кг (×1.5)"""
        cost, _ = calculate_delivery_cost(25.0, 1000, "обычный")
        self.assertEqual(cost, 7800)

    def test_fragile_package_surcharge(self):
        """4. Хрупкая посылка (+300)"""
        cost, _ = calculate_delivery_cost(2.0, 1000, "хрупкий")
        self.assertEqual(cost, 5500)

    def test_dangerous_package_surcharge(self):
        """5. Опасная посылка (+1000)"""
        cost, _ = calculate_delivery_cost(2.0, 1000, "опасный")
        self.assertEqual(cost, 6200)

    def test_express_delivery(self):
        """6. Экспресс-доставка (×0.5 и срок //2)"""
        cost, date = calculate_delivery_cost(2.0, 1000, "обычный", is_express=True)
        self.assertEqual(cost, 2600)
        self.assertEqual(date, "2026-09-04")

    def test_minimum_delivery_days(self):
        """7. Минимальный срок — 1 день (маленькое расстояние)"""
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_weight_too_small(self):
        """8. Вес меньше 0.1 кг — ошибка"""
        cost, date = calculate_delivery_cost(0.05, 1000, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_too_large(self):
        """9. Вес больше 50 кг — ошибка"""
        cost, date = calculate_delivery_cost(60.0, 1000, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_package_type(self):
        """10. Неверный тип посылки — ошибка"""
        cost, date = calculate_delivery_cost(2.0, 1000, "стеклянный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_too_large(self):
        """Дистанция больше 5000 км — ошибка"""
        cost, date = calculate_delivery_cost(2.0, 6000, "обычный")
        self.assertEqual(cost, -1)

    def test_dangerous_heavy_express_combo(self):
        """Опасный + тяжёлый + экспресс — комбинация надбавок"""
        cost, _ = calculate_delivery_cost(25.0, 1000, "опасный", is_express=True)
        self.assertEqual(cost, 4400)


if __name__ == "__main__":
    unittest.main()
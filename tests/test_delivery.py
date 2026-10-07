import unittest
from src.Delivery import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):

    def test_weight_below_minimum_returns_error(self):
        """1. Вес меньше 0.1 кг -> ошибка"""
        cost, date = calculate_delivery_cost(0.05, 1000, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_maximum_returns_error(self):
        """2. Вес больше 50 кг -> ошибка"""
        cost, date = calculate_delivery_cost(60.0, 1000, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_above_maximum_returns_error(self):
        """3. Дистанция больше 5000 км -> ошибка"""
        cost, _ = calculate_delivery_cost(2.0, 6000, "обычный")
        self.assertEqual(cost, -1)

    def test_unknown_package_type_returns_error(self):
        """4. Неизвестный тип посылки -> ошибка"""
        cost, _ = calculate_delivery_cost(2.0, 1000, "стеклянный")
        self.assertEqual(cost, -1)

    def test_basic_delivery_cost(self):
        """5. Обычная посылка, без надбавок: 200 + 5*км"""
        cost, _ = calculate_delivery_cost(2.0, 1000, "обычный")
        self.assertEqual(cost, 5200)

    def test_medium_weight_surcharge(self):
        """6. Вес 10 кг -> надбавка ×1.2"""
        cost, _ = calculate_delivery_cost(10.0, 1000, "обычный")
        self.assertEqual(cost, 6240)

    def test_heavy_weight_surcharge(self):
        """7. Вес 25 кг -> надбавка ×1.5"""
        cost, _ = calculate_delivery_cost(25.0, 1000, "обычный")
        self.assertEqual(cost, 7800)

    def test_fragile_surcharge(self):
        """8. Хрупкая посылка -> +300"""
        cost, _ = calculate_delivery_cost(2.0, 1000, "хрупкий")
        self.assertEqual(cost, 5500)

    def test_dangerous_surcharge(self):
        """9. Опасная посылка -> +1000"""
        cost, _ = calculate_delivery_cost(2.0, 1000, "опасный")
        self.assertEqual(cost, 6200)

    def test_express_should_cost_more(self):
        """10. БАГ: экспресс должен УДОРОЖАТЬ доставку, а не удешевлять.
        В коде: total_cost *= 0.5. Ожидание: цена выше обычной."""
        cost_normal, _ = calculate_delivery_cost(2.0, 1000, "обычный")
        cost_express, _ = calculate_delivery_cost(2.0, 1000, "обычный", is_express=True)
        self.assertGreater(cost_express, cost_normal)

    def test_express_should_be_faster(self):
        """11. Экспресс должен приехать раньше обычной доставки"""
        _, date_normal = calculate_delivery_cost(2.0, 1000, "обычный")
        _, date_express = calculate_delivery_cost(2.0, 1000, "обычный", is_express=True)
        self.assertLess(date_express, date_normal)

    def test_minimum_delivery_one_day(self):
        """12. Даже при малой дистанции срок >= 1 дня"""
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_cost_rounded_not_truncated(self): 
        """13. БАГ: int() отбрасывает копейки, должно быть round().
        ×1.5: 705*1.5 = 1057.5 -> int=1057, round=1058"""
        cost, _ = calculate_delivery_cost(25.0, 101, "обычный")
        self.assertEqual(cost, 1058)


    def test_exact_minimum_weight(self):
        """14. Ровно 0.1 кг — валидно"""
        cost, _ = calculate_delivery_cost(0.1, 1000, "обычный")
        self.assertNotEqual(cost, -1)

    def test_exact_minimum_distance(self):
        """15. Ровно 1 км — валидно"""
        cost, _ = calculate_delivery_cost(2.0, 1, "обычный")
        self.assertNotEqual(cost, -1)

    def test_exact_maximum_bounds(self):
        """16. Ровно 50 кг и 5000 км — валидно"""
        cost, _ = calculate_delivery_cost(50.0, 5000, "обычный")
        self.assertNotEqual(cost, -1)


if __name__ == "__main__":
    unittest.main()
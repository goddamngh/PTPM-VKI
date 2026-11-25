import logging
from src.triangle import get_triangle_type_and_coords
from src.interfaces import UserInteraction, ExternalDependency


class Controller:
    """Контроллер, реализующий сквозной сценарий работы приложения."""

    def __init__(
        self,
        user_interaction: UserInteraction,
        db,
        external_dependency: ExternalDependency,
    ):
        self.user_interaction = user_interaction
        self.db = db
        self.external_dependency = external_dependency

    def process_triangle(self) -> str:
        """Один сквозной сценарий: ввод → БД/вычисление → отправка → результат."""
        a_str = self.user_interaction.get_input("Сторона A: ")
        b_str = self.user_interaction.get_input("Сторона B: ")
        c_str = self.user_interaction.get_input("Сторона C: ")

        # Пытаемся найти запись в БД (нужны float-значения сторон)
        try:
            a, b, c = float(a_str), float(b_str), float(c_str)
            record = self.db.get_record(a, b, c)
        except (ValueError, TypeError):
            record = None

        if record:
            tri_type, error_msg = record
            logging.info(f"Результат взят из БД: тип={tri_type}")
        else:
            tri_type, coords = get_triangle_type_and_coords(a_str, b_str, c_str)
            error_msg = ""
            if tri_type == "не треугольник":
                error_msg = "не треугольник"
            elif tri_type == "":
                error_msg = "нечисловые данные"

            try:
                a, b, c = float(a_str), float(b_str), float(c_str)
                self.db.add_record(a, b, c, tri_type, error_msg)
                logging.info(f"Результат сохранён в БД: тип={tri_type}")
            except (ValueError, TypeError):
                logging.info(f"Нечисловые данные не сохранены в БД")

        result = f"Тип: {tri_type}" if tri_type else "Ошибка: нечисловые данные"
        self.external_dependency.send_data(result)
        return result
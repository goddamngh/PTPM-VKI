import logging
import sys
import os

# --- НАСТРОЙКА ЛОГИРОВАНИЯ ---
if not os.path.exists("logs"):
    os.makedirs("logs")

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)


def get_triangle_type_and_coords(a_str, b_str, c_str):
    logging.info(f"Запрос: A={a_str}, B={b_str}, C={c_str}")

    try:
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)
    except ValueError:
        logging.error(f"Ошибка: нечисловые данные (A={a_str}, B={b_str}, C={c_str})")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        logging.error("Ошибка: стороны должны быть положительными")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        logging.info("Результат: не треугольник (нарушено неравенство треугольника)")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b == c:
        t_type = "равносторонний"
    elif a == b or b == c or a == c:
        t_type = "равнобедренный"
    else:
        t_type = "разносторонний"

    max_side = max(a, b, c)
    scale = 80.0 / max_side

    ax, ay = 10, 90
    bx, by = int(10 + a * scale), 90
    cx = int(10 + (a * scale) / 2)
    cy = int(90 - (b * scale))

    coords = [
        (max(0, min(100, ax)), max(0, min(100, ay))),
        (max(0, min(100, bx)), max(0, min(100, by))),
        (max(0, min(100, cx)), max(0, min(100, cy)))
    ]

    logging.info(f"Результат: тип={t_type}, координаты={coords}")
    return t_type, coords


def main():
    logging.info("Приложение запущено")
    logging.info("Логгер успешно сконфигурирован")

    print("--- Введите длины сторон треугольника ---")
    try:
        a_str = input("Сторона A: ")
        b_str = input("Сторона B: ")
        c_str = input("Сторона C: ")
    except Exception as e:
        logging.critical(f"Критическая ошибка ввода: {e}")
        return

    tri_type, coords = get_triangle_type_and_coords(a_str, b_str, c_str)

    print(f"\nТип треугольника: {tri_type if tri_type else 'нечисловые данные'}")
    print(f"Координаты вершин: {coords}")


if __name__ == "__main__":
    main()
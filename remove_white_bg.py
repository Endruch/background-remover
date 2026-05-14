#!/usr/bin/env python3
"""
Скрипт для удаления белого фона с изображений и сохранения в PNG формат с прозрачностью.
Сохраняет градиент как альфа-канал (полупрозрачность).
"""

from PIL import Image
import os
import sys


def remove_white_background(input_path, output_path=None, threshold=240):
    """
    Удаляет белый фон с изображения и сохраняет как GIF с прозрачностью.

    Args:
        input_path: путь к входному файлу изображения
        output_path: путь к выходному PNG файлу (по умолчанию добавляет _transparent.png)
        threshold: не используется в текущей версии
    """
    # Открываем изображение
    img = Image.open(input_path)

    # Конвертируем в Grayscale (оттенки серого) - одноканальный режим
    grayscale = img.convert("L")

    # Получаем данные пикселей (каждый пиксель - одно число 0-255)
    gray_data = grayscale.getdata()

    # Создаем RGBA изображение для результата
    result = Image.new("RGBA", img.size)
    new_data = []

    for gray_value in gray_data:
        # gray_value: 0 (чёрный) ... 255 (белый)
        # Нужно: чёрный → непрозрачный, белый → прозрачный
        #
        # Инвертируем: чем ТЕМНЕЕ (меньше gray_value), тем БОЛЬШЕ alpha
        # 0 (чёрный) → alpha = 255 - 0 = 255 (непрозрачный)
        # 100 (серый) → alpha = 255 - 100 = 155 (полупрозрачный)
        # 255 (белый) → alpha = 255 - 255 = 0 (прозрачный)

        alpha = 255 - gray_value

        # Все пиксели чёрные, прозрачность по градиенту
        new_data.append((0, 0, 0, alpha))

    # Применяем новые данные к результату
    result.putdata(new_data)

    # Определяем путь для сохранения
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_transparent.png"

    # Сохраняем как PNG (поддерживает полупрозрачность!)
    # GIF не поддерживает градиент прозрачности - только полностью прозрачный/непрозрачный
    result.save(output_path, "PNG", optimize=True)
    print(f"Сохранено: {output_path}")


def process_directory(directory, threshold=240):
    """
    Обрабатывает все JPEG файлы в директории.

    Args:
        directory: путь к директории
        threshold: порог для определения белого цвета
    """
    jpeg_extensions = ('.jpg', '.jpeg', '.JPG', '.JPEG')

    for filename in os.listdir(directory):
        if filename.endswith(jpeg_extensions):
            input_path = os.path.join(directory, filename)
            print(f"Обработка: {input_path}")
            try:
                remove_white_background(input_path, threshold=threshold)
            except Exception as e:
                print(f"Ошибка при обработке {input_path}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python remove_white_bg.py <файл.jpg>")
        print("  python remove_white_bg.py <файл.jpg> <выходной.gif>")
        print("  python remove_white_bg.py <директория>")
        print("  python remove_white_bg.py <файл.jpg> --threshold 220")
        sys.exit(1)

    path = sys.argv[1]
    threshold = 240

    # Проверяем параметр threshold
    if "--threshold" in sys.argv:
        threshold_index = sys.argv.index("--threshold")
        if threshold_index + 1 < len(sys.argv):
            threshold = int(sys.argv[threshold_index + 1])

    if os.path.isfile(path):
        # Обрабатываем один файл
        output_path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
        remove_white_background(path, output_path, threshold)
    elif os.path.isdir(path):
        # Обрабатываем все JPEG в директории
        process_directory(path, threshold)
    else:
        print(f"Ошибка: {path} не является файлом или директорией")
        sys.exit(1)

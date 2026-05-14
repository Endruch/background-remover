#!/usr/bin/env python3
"""
Скрипт для конвертации изображения в ICO файл для Windows
"""

from PIL import Image
import sys
import os


def convert_to_ico(input_path, output_path="app_icon.ico"):
    """
    Конвертирует изображение в ICO формат с несколькими размерами

    Args:
        input_path: путь к входному файлу (GIF, PNG, JPG и т.д.)
        output_path: путь к выходному ICO файлу
    """
    try:
        # Открываем изображение
        img = Image.open(input_path)

        # Конвертируем в RGBA если нужно
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Создаём несколько размеров для иконки
        # Windows использует разные размеры в разных местах
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

        # Создаём список изображений разных размеров
        icon_images = []
        for size in icon_sizes:
            # Создаём копию и изменяем размер
            resized = img.copy()
            resized.thumbnail(size, Image.Resampling.LANCZOS)

            # Если изображение меньше нужного размера, центрируем его
            if resized.size != size:
                new_img = Image.new('RGBA', size, (0, 0, 0, 0))
                paste_x = (size[0] - resized.size[0]) // 2
                paste_y = (size[1] - resized.size[1]) // 2
                new_img.paste(resized, (paste_x, paste_y))
                resized = new_img

            icon_images.append(resized)

        # Сохраняем как ICO
        # Начинаем с самого большого размера для лучшего качества
        icon_images[-1].save(
            output_path,
            format='ICO',
            sizes=[img.size for img in icon_images],
            append_images=icon_images[:-1]
        )

        print(f"✓ Иконка успешно создана: {output_path}")
        print(f"  Размеры: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")

        # Показываем размер файла
        file_size = os.path.getsize(output_path) / 1024
        print(f"  Размер файла: {file_size:.1f} KB")

        return True

    except Exception as e:
        print(f"✗ Ошибка при создании иконки: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python create_icon.py <файл_изображения>")
        print("Пример: python create_icon.py Mad6d.gif")
        print("\nСоздаст файл app_icon.ico для использования в сборке")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"✗ Файл не найден: {input_file}")
        sys.exit(1)

    # Создаём иконку
    output_file = "app_icon.ico"
    success = convert_to_ico(input_file, output_file)

    if success:
        print(f"\n✓ Готово! Используйте файл '{output_file}' при сборке EXE")
    else:
        sys.exit(1)

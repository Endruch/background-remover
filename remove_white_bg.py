#!/usr/bin/env python3

from PIL import Image
import os
import sys


def remove_white_background(input_path, output_path=None, threshold=240):
    img = Image.open(input_path)

    grayscale = img.convert("L")

    gray_data = grayscale.getdata()

    result = Image.new("RGBA", img.size)
    new_data = []

    for gray_value in gray_data:
        alpha = 255 - gray_value
        new_data.append((0, 0, 0, alpha))

    result.putdata(new_data)

    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_transparent.png"

    result.save(output_path, "PNG", optimize=True)
    print(f"Сохранено: {output_path}")


def process_directory(directory, threshold=240):
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

    if "--threshold" in sys.argv:
        threshold_index = sys.argv.index("--threshold")
        if threshold_index + 1 < len(sys.argv):
            threshold = int(sys.argv[threshold_index + 1])

    if os.path.isfile(path):
        output_path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
        remove_white_background(path, output_path, threshold)
    elif os.path.isdir(path):
        process_directory(path, threshold)
    else:
        print(f"Ошибка: {path} не является файлом или директорией")
        sys.exit(1)

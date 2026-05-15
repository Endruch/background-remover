#!/usr/bin/env python3

from PIL import Image
import sys
import os


def convert_to_ico(input_path, output_path="app_icon.ico"):
    try:
        img = Image.open(input_path)

        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

        icon_images = []
        for size in icon_sizes:
            resized = img.copy()
            resized.thumbnail(size, Image.Resampling.LANCZOS)

            if resized.size != size:
                new_img = Image.new('RGBA', size, (0, 0, 0, 0))
                paste_x = (size[0] - resized.size[0]) // 2
                paste_y = (size[1] - resized.size[1]) // 2
                new_img.paste(resized, (paste_x, paste_y))
                resized = new_img

            icon_images.append(resized)

        icon_images[-1].save(
            output_path,
            format='ICO',
            sizes=[img.size for img in icon_images],
            append_images=icon_images[:-1]
        )

        print(f"✓ Icon successfully created: {output_path}")
        print(f"  Sizes: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")

        file_size = os.path.getsize(output_path) / 1024
        print(f"  File size: {file_size:.1f} KB")

        return True

    except Exception as e:
        print(f"✗ Error creating icon: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_icon.py <image_file>")
        print("Example: python create_icon.py Mad6d.gif")
        print("\nWill create app_icon.ico file for use in build")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"✗ File not found: {input_file}")
        sys.exit(1)

    output_file = "app_icon.ico"
    success = convert_to_ico(input_file, output_file)

    if success:
        print(f"\n✓ Done! Use '{output_file}' file when building EXE")
    else:
        sys.exit(1)

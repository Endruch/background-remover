#!/usr/bin/env python3
"""
GUI приложение для удаления белого фона с изображений.
Поддерживает drag-and-drop и предпросмотр.
"""

import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os
import sys


class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("")  # Пустой заголовок
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        self.current_image_path = None
        self.preview_image = None

        self._create_widgets()

    def _create_widgets(self):
        """Создаем интерфейс"""

        # Область для drag-and-drop
        self.drop_frame = tk.Frame(
            self.root,
            width=350,
            height=300,
            bg="#f0f0f0",
            relief=tk.RIDGE,
            borderwidth=2
        )
        self.drop_frame.pack(pady=20, padx=25)
        self.drop_frame.pack_propagate(False)

        # Регистрируем drag-and-drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self._on_drop)

        # Текст подсказки внутри области
        self.hint_label = tk.Label(
            self.drop_frame,
            text="Перетащите сюда\nизображение",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#888888"
        )
        self.hint_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Label для превью изображения
        self.preview_label = tk.Label(self.drop_frame, bg="#f0f0f0")
        self.preview_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Кнопка обработки
        self.process_button = tk.Button(
            self.root,
            text="Убрать фон",
            font=("Arial", 12, "bold"),
            command=self._process_image,
            width=25,
            height=2,
            bg="#2196F3",
            fg="white",
            cursor="hand2",
            state=tk.DISABLED
        )
        self.process_button.pack(pady=15)

    def _on_drop(self, event):
        """Обработка перетаскивания файла"""
        # Получаем путь к файлу (может быть в фигурных скобках)
        file_path = event.data

        # Убираем фигурные скобки если есть
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]

        self._load_image(file_path)

    def _load_image(self, file_path):
        """Загрузка и отображение превью"""
        try:
            # Проверяем существование файла
            if not os.path.exists(file_path):
                messagebox.showerror("Ошибка", f"Файл не найден:\n{file_path}")
                return

            # Открываем изображение
            img = Image.open(file_path)

            # Сохраняем путь
            self.current_image_path = file_path

            # Создаем превью (максимум 320x270 для компактного окна)
            img.thumbnail((320, 270), Image.Resampling.LANCZOS)

            # Конвертируем для tkinter
            self.preview_image = ImageTk.PhotoImage(img)

            # Показываем превью
            self.hint_label.place_forget()
            self.preview_label.config(image=self.preview_image)
            self.preview_label.image = self.preview_image

            # Активируем кнопку обработки
            self.process_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{str(e)}")

    def _process_image(self):
        """Обработка изображения - удаление фона"""
        if not self.current_image_path:
            messagebox.showwarning("Предупреждение", "Сначала выберите изображение")
            return

        try:
            # Отключаем кнопку во время обработки
            self.process_button.config(state=tk.DISABLED, text="Обработка...")
            self.root.update()

            # Открываем изображение
            img = Image.open(self.current_image_path)

            # Конвертируем в Grayscale
            grayscale = img.convert("L")
            gray_data = grayscale.getdata()

            # Создаем RGBA изображение для результата
            result = Image.new("RGBA", img.size)
            new_data = []

            for gray_value in gray_data:
                # Инвертируем яркость для получения прозрачности
                alpha = 255 - gray_value
                # Все пиксели чёрные, прозрачность по градиенту
                new_data.append((0, 0, 0, alpha))

            # Применяем новые данные
            result.putdata(new_data)

            # Формируем имя выходного файла
            base_name = os.path.splitext(self.current_image_path)[0]
            output_path = f"{base_name}_transparent.png"

            # Сохраняем
            result.save(output_path, "PNG", optimize=True)

            # Возвращаем кнопку в исходное состояние
            self.process_button.config(state=tk.NORMAL, text="Убрать фон")

            # Показываем краткое сообщение об успехе (без блокировки)
            messagebox.showinfo(
                "Готово",
                f"Сохранено: {os.path.basename(output_path)}"
            )

            # Можно сразу загружать следующее изображение!

        except Exception as e:
            self.process_button.config(state=tk.NORMAL, text="Убрать фон")
            messagebox.showerror("Ошибка", f"Не удалось обработать изображение:\n{str(e)}")


def main():
    """Запуск приложения"""
    try:
        root = TkinterDnD.Tk()
        app = BackgroundRemoverApp(root)
        root.mainloop()
    except Exception as e:
        # Если tkinterdnd2 не работает, показываем сообщение
        print(f"Ошибка запуска: {e}")
        print("\nВозможно, не установлен модуль tkinterdnd2")
        print("Установите: pip install tkinterdnd2")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)


if __name__ == "__main__":
    main()

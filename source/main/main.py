import tkinter as tk
from tkinter import filedialog, scrolledtext
import re


def parse_source_file(content):
    """Извлекает секции из файла по меткам"""
    # Паттерн для Source file
    source_pattern = r'## Source file\s*```.*?\n(.*?)```'
    source_code = re.search(source_pattern, content, flags=re.DOTALL)
    source_code = source_code.group(1).strip() if source_code else ''

    # Паттерн для match
    match_pattern = r'### match:\s*```.*?\n(.*?)```'
    match_block = re.search(match_pattern, content, flags=re.DOTALL)
    match_block = match_block.group(1).strip() if match_block else ''

    # Паттерн для patch
    patch_pattern = r'### patch\s*```.*?\n(.*?)```'
    patch_code = re.search(patch_pattern, content, flags=re.DOTALL)
    patch_code = patch_code.group(1).strip() if patch_code else ''

    return source_code, match_block, patch_code


def apply_patch(source, match_block, patch_code):
    """Применяет патч к исходному коду с учетом правил match"""
    match_lines = match_block.splitlines()
    source_lines = source.splitlines()
    patched_lines = []
    inserting_start = False
    inserting_end = False

    i = 0
    while i < len(source_lines):
        line = source_lines[i]
        if not match_lines:
            # Если закончились строки в match, просто добавляем оставшийся исходный код
            patched_lines.extend(source_lines[i:])
            break

        match_line = match_lines[0].strip()

        if match_line == '...':
            # Пропустить строку, перейти к следующей строке match
            match_lines.pop(0)
            patched_lines.append(line)
        elif '>>>' in match_line:
            # Вставка патча в начале функции или перед конкретной строкой
            if not inserting_start:
                patched_lines.append(patch_code)  # Вставляем патч
                inserting_start = True
            patched_lines.append(line)  # Добавляем строку после вставки
            match_lines.pop(0)
        elif re.match(match_line.replace('...', '.*'), line):
            # Совпадение строки, переходим к следующей строке match
            patched_lines.append(line)
            match_lines.pop(0)
        elif line.strip() == '}':
            # Найдена закрывающая скобка — вставляем патч в конец
            if not inserting_end:
                patched_lines.append(patch_code)  # Вставляем патч перед закрывающей скобкой
                inserting_end = True
            patched_lines.append(line)
        else:
            patched_lines.append(line)

        i += 1

    return "\n".join(patched_lines)


class CodePatcherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Code Patcher")
        self.geometry("1200x600")

        # Инициализация данных
        self.source_code = ""
        self.match_block = ""
        self.patch_code = ""

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Панель управления
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10, fill=tk.X)

        tk.Button(control_frame, text="Load Source File", command=self.load_file).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Apply Patch", command=self.apply_patch).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Save Patched File", command=self.save_file).pack(side=tk.LEFT, padx=10)

        # Текстовые области
        text_frame = tk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Создание трех колонок
        self.text_areas = {}
        for col, title in enumerate(["Source Code", "Match Block", "Patch Code"]):
            frame = tk.Frame(text_frame)
            frame.grid(row=0, column=col, sticky="nsew", padx=5)
            text_frame.grid_columnconfigure(col, weight=1)

            tk.Label(frame, text=title).pack(anchor="w")
            text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True)
            self.text_areas[title] = text_widget

    def load_file(self):
        """Загрузка и обработка файла"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return

        with open(file_path, 'r') as f:
            content = f.read()
            self.source_code, self.match_block, self.patch_code = parse_source_file(content)
            self.update_text_areas()

    def apply_patch(self):
        """Применение патча и отображение результата"""
        if not all([self.source_code, self.match_block, self.patch_code]):
            return

        modified_code = apply_patch(self.source_code, self.match_block, self.patch_code)
        self.show_result(modified_code)

    def update_text_areas(self):
        """Обновление текстовых полей"""
        self.text_areas["Source Code"].delete(1.0, tk.END)
        self.text_areas["Source Code"].insert(tk.END, self.source_code)

        self.text_areas["Match Block"].delete(1.0, tk.END)
        self.text_areas["Match Block"].insert(tk.END, self.match_block)

        self.text_areas["Patch Code"].delete(1.0, tk.END)
        self.text_areas["Patch Code"].insert(tk.END, self.patch_code)

    def show_result(self, result):
        """Отображение результата в новом окне"""
        result_window = tk.Toplevel(self)
        result_window.title("Patched Result")
        result_window.geometry("800x600")

        text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, result)

    def save_file(self):
        """Сохранение патченного файла"""
        if not self.source_code:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return

        modified_code = apply_patch(self.source_code, self.match_block, self.patch_code)
        with open(file_path, 'w') as f:
            f.write(modified_code)


if __name__ == "__main__":
    app = CodePatcherApp()
    app.mainloop()
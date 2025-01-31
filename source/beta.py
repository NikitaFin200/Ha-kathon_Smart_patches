import tkinter as tk
from tkinter import filedialog
import re


def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    sections = {'source': '', 'match': '', 'patch': ''}
    current_section = None

    for line in content.split('\n'):
        if line.startswith('## Source file'):
            current_section = 'source'
        elif line.startswith('### match:'):
            current_section = 'match'
        elif line.startswith('### patch'):
            current_section = 'patch'
        elif line.startswith('## Result'):
            current_section = None  # Игнорируем result
        elif current_section:
            sections[current_section] += line + '\n'

    return {key: sections[key].strip() for key in sections}


def tokenize(code):
    """
    Токенизируем код. Преобразуем его в список токенов.
    """
    token_pattern = re.compile(r'(\w+|\S)')  # Делим код на слова и знаки препинания
    tokens = token_pattern.findall(code)
    return tokens


def apply_patch(source, match, patch):
    """
    Применяем патч к исходному коду по логике с токенами и операторами '...' и '>>>'
    """
    source_lines = source.split('\n')
    match_lines = match.split('\n')
    patch_lines = patch.split('\n')

    # Поиск строки, содержащей '>>>', для вставки патча
    for i, line in enumerate(match_lines):
        if '>>>' in line:
            # Мы нашли строку с '>>>', теперь вставляем патч после этой строки
            insertion_point = i
            break
    else:
        # Если не нашли '>>>', то просто возвращаем исходный код
        return source

    # Разделяем исходный код на строки
    modified_code = []
    # Добавляем строки до точки вставки
    modified_code.extend(source_lines[:insertion_point])
    # Вставляем патч
    modified_code.extend(patch_lines)
    # Добавляем оставшуюся часть исходного кода
    modified_code.extend(source_lines[insertion_point:])

    return '\n'.join(modified_code)


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[('Markdown Files', '*.md')])
    if not file_path:
        return

    # Разбираем файл и получаем блоки
    global sections
    sections = parse_markdown(file_path)

    # Заполняем текстовые поля в GUI
    source_text.delete('1.0', tk.END)
    source_text.insert(tk.END, sections['source'])

    match_text.delete('1.0', tk.END)
    match_text.insert(tk.END, sections['match'])

    patch_text.delete('1.0', tk.END)
    patch_text.insert(tk.END, sections['patch'])


def apply_patch_button():
    updated_code = apply_patch(sections['source'], sections['match'], sections['patch'])
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, updated_code)


# Создание GUI
root = tk.Tk()
root.title("Markdown Patch Application Tool")

# Кнопки для открытия файла и применения патча
tk.Button(root, text="Open Markdown File", command=open_file).pack()
tk.Button(root, text="Apply Patch", command=apply_patch_button).pack()

# Сетка для отображения исходного кода, совпадений и патча
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Source Code").grid(row=0, column=0)
tk.Label(frame, text="Match Rules").grid(row=0, column=1)
tk.Label(frame, text="Patch").grid(row=0, column=2)

grid_options = {'wrap': tk.WORD, 'height': 20, 'width': 40}

source_text = tk.Text(frame, **grid_options)
source_text.grid(row=1, column=0)
match_text = tk.Text(frame, **grid_options)
match_text.grid(row=1, column=1)
patch_text = tk.Text(frame, **grid_options)
patch_text.grid(row=1, column=2)

# Результат
result_text = tk.Text(root, wrap=tk.WORD, height=20, width=100)
result_text.pack()

# Запуск основного цикла приложения
root.mainloop()

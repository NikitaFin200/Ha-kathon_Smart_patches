import re

def load_code_from_markdown(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Регулярное выражение для поиска блока match
    match_pattern = re.compile(r'### match:\s*```(.*?)```', re.DOTALL)
    # Регулярное выражение для поиска блока patch
    patch_pattern = re.compile(r'### patch\s*```(.*?)```', re.DOTALL)

    # Поиск match и patch
    match = match_pattern.search(content)
    patch = patch_pattern.search(content)

    # Извлечение и очистка текста
    match_text = match.group(1).strip() if match else None
    patch_text = patch.group(1).strip() if patch else None

    return match_text, patch_text

def parse_match_string(match_text: str):
    # Регулярное выражение для поиска операторов (..., <<<, >>>) и их аргументов
    pattern = re.compile(r'(\.{3}|<<<|>>>)(.*?)(?=(\.{3}|<<<|>>>|$))', re.DOTALL)

    # Найти все совпадения
    tokens = pattern.findall(match_text)

    # Преобразовать результат в список кортежей
    parsed_result = [(op, arg) for op, arg, _ in tokens]

    return parsed_result

filepath = "add_function_beg.md"
match, patch = load_code_from_markdown(filepath)
parsed_output = parse_match_string(match)
print("Match:", parsed_output)
print("Patch:", patch)

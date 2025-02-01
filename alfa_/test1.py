import re
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token, is_token_subtype

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
    # Извлечение и очистка текста ffff
    match_text = match.group(1).strip() if match else None
    patch_text = patch.group(1).strip() if patch else None
    return match_text, patch_text

def tokenize_code(code, language):
    try:
        lexer = get_lexer_by_name(language)
        tokens = []

        special_operators = {"...", ">>>", "<<<"}
        pattern = re.compile(r'(\.\.\.|>>>|<<<)')

        # Разбиваем код по операторам, сохраняя их
        parts = pattern.split(code)

        for part in parts:
            if part in special_operators:
                tokens.append((Token.Operator, part))
            else:
                tokens.extend(lex(part, lexer))

        return tokens
    except Exception as e:
        return f"Ошибка: {str(e)}"

def transform_tuples(input_tuples, func, extra_param):
    return [(operator, func(value, extra_param)) for operator, value in input_tuples]


def source_to_tokenList(file_path, func, extra_param):
    result_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            processed_string = remove_insignificant_tokens(func(line, extra_param), extra_param)
            result_list.append(processed_string)

    return result_list

def remove_insignificant_tokens(token_list, language):
    filtered = []
    is_leading = True  # Флаг для отслеживания начала строки

    for token_type, token_value in token_list:
        if is_token_subtype(token_type, Token.Text.Whitespace) and token_value == '\n':
            continue        # Обработка для Python
        if language.lower() == 'python':
            if is_token_subtype(token_type, Token.Text):
                # Сохраняем только ведущие пробелы
                if is_leading:
                    filtered.append((token_type, token_value))
            else:
                # Сохраняем все значимые токены
                filtered.append((token_type, token_value))
                # После первого не-пробельного токена выключаем режим leading
                is_leading = False

        # Обработка для остальных языков
        else:
            filtered.append((token_type, token_value))

    return filtered
def remove_in_tok_match(filepath, language):
    match, patch = load_code_from_markdown(filepath)
    match = match.split('\n')
    token = []
    token_list = []
    for mch in match:
        token = remove_insignificant_tokens(tokenize_code(mch, language), language)
        token_list.extend(token)
    token_list = group_tokens(token_list)
    return token_list

    # Найти все совпадения
from collections import defaultdict

def group_tokens(tokens):
    result = []
    current_operator = None
    current_group = []

    for token in tokens:
        token_type, token_value = token

        if is_token_subtype(token_type, Token.Operator) and token_value in ['...', '>>>', '<<<']:
            if current_group or current_operator is not None:
                result.append((current_operator, current_group))
                current_group = []
            current_operator = token_value
        else:
            current_group.append(token)

    # Добавляем последнюю группу, если есть оператор или группа токенов
    if current_operator is not None or current_group:
        result.append((current_operator, current_group))

    return result


def compute_lps(pattern):
    """Создает префиксный массив для подсписка (Longest Prefix Suffix)."""
    lps = [0] * len(pattern)
    length = 0  # Длина предыдущего наибольшего префикса-суффикса
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def compute_lps(pattern):
    """Создает префиксный массив для подсписка (Longest Prefix Suffix)."""
    lps = [0] * len(pattern)
    length = 0  # Длина предыдущего наибольшего префикса-суффикса
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search_2d(text, pattern):
    """Ищет все вхождения подсписка pattern в 2D списке text."""
    if not pattern:
        return []

    lps = compute_lps(pattern)
    result = []
    i = j = 0  # i - индекс в text, j - в pattern

    # Преобразуем 2D список в 1D список для удобства поиска
    flat_text = []
    index_map = []  # Для хранения соответствия индексов [i, j]

    for row_idx, row in enumerate(text):
        for col_idx, value in enumerate(row):
            flat_text.append(value)
            index_map.append((row_idx, col_idx))

    # Поиск с использованием KMP
    while i < len(flat_text):
        if flat_text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                # Найдено вхождение
                start_idx = i - j
                # Получаем начальные индексы [i, j] для первого элемента pattern
                row_idx, col_idx = index_map[start_idx]
                result.append([row_idx, col_idx])
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result

filepath = "../tests/py/py_add_end.md"
file_path = "../source/hatch/expressions.py"
match, patch = load_code_from_markdown(filepath)
tr3 = source_to_tokenList(file_path, tokenize_code, "python")
tr4 =  remove_in_tok_match(filepath, "python")

print(tr4)
# print(parsed_output)
# print("Match:", tr)
# print("Patch:", patch)
print("Sourse:",  tr3)
print(kmp_search_2d(tr3, tr4[0][1]))

from tabnanny import Whitespace

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
   # match_text = match_text.replace("\n","")
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
            if re.fullmatch(r'\s*', line):
                continue
            processed_string = remove_insignificant_tokens(func(line, extra_param), extra_param)
            if processed_string == [(Token.Text, '    ')]:
                continue
            else:
                result_list.append(processed_string)

    return result_list

def remove_insignificant_tokens(token_list, language):
    filtered = []
    is_leading = True  # Флаг для отслеживания начала строки

    for token_type, token_value in token_list:
        # Всегда пропускаем комментарии
        if is_token_subtype(token_type, Token.Comment):
            continue
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
            if not is_token_subtype(token_type, Token.Text):
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

        # Проверяем, является ли токен оператором (например, '...', '>>>', '<<<')
        if is_token_subtype(token_type, Token.Operator) and token_value in ['...', '>>>', '<<<']:
            print(token_type)
            # Если есть текущая группа, добавляем ее в результат
            if current_group:
                result.append((current_operator, current_group))
                current_group = []  # Очистить текущую группу

            # Устанавливаем текущий оператор
            current_operator = token_value
        else:
            # Добавляем токен в текущую группу
            current_group.append(token)

    # Добавляем последнюю группу
    if current_group:
        result.append((current_operator, current_group))

    return result
def ser
filepath = "add_function_end.md"
file_path = "expressions.py"
match, patch = load_code_from_markdown(filepath)
parsed_output = parse_match_string(match)
tr = transform_tuples(parsed_output, tokenize_code, "cpp")
tr3 = source_to_tokenList(file_path, tokenize_code, "python")
tr4 =  remove_in_tok_match(filepath, "python")
print(tr4)
# print(parsed_output)
# print("Match:", tr)
# print("Patch:", patch)
print("Sourse:",  tr3)
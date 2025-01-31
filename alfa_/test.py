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

    source_pattern = re.compile(r'## Source file\s*```(.*?)```', re.DOTALL)
    # Поиск match и patch
    match = match_pattern.search(content)
    patch = patch_pattern.search(content)
    source = source_pattern.search(content)
    # Извлечение и очистка текста ffff
    match_text = match.group(1).strip() if match else None
    match_text = match_text.replace("\n", "")
    patch_text = patch.group(1).strip() if patch else None
    source_text = source.group(1).strip() if source else None
    return match_text, patch_text, source_text

def parse_match_string(match_text: str):
    # Регулярное выражение для поиска операторов (..., <<<, >>>) и их аргументов
    pattern = re.compile(r'(\.{3}|<<<|>>>)(.*?)(?=(\.{3}|<<<|>>>|$))', re.DOTALL)

    # Найти все совпадения
    tokens = pattern.findall(match_text)

    # Преобразовать результат в список кортежей
    parsed_result = [(op, re.sub(r'\s+', ' ', arg).strip()) for op, arg, _ in tokens]

    return parsed_result
def tokenize_code(code, language):
    try:
        lexer = get_lexer_by_name(language)
        tokens = lex(code, lexer)
        return list(tokens)
    except Exception as e:
        return f"Ошибка: {str(e)}"


def transform_tuples(input_tuples, func, extra_param):
    def clean_tokens(tokens):
        cleaned = []
        previous_was_whitespace = False

        for token_type, token_value in tokens:
            if is_token_subtype(token_type, Token.Text.Whitespace):
                if not previous_was_whitespace:
                    previous_was_whitespace = True
                    continue  # Убираем лишний пробел
            else:
                previous_was_whitespace = False
                cleaned.append((token_type, token_value))

        return cleaned

    return [(operator, clean_tokens(func(value, extra_param))) for operator, value in input_tuples]



def source_to_tokenList(file_path, func, extra_param):
    result_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if re.fullmatch(r'\s*', line):
                continue
            if re.fullmatch(r'\[\(Token\.Text,\s*\'\s*\'\)\]', str(line)):
                continue


            processed_string = remove_insignificant_tokens(func(line, extra_param), extra_param)
            if processed_string == [(Token.Text, '    ')]:
                continue
            else:
                result_list.append(processed_string)


    return result_list

def remove_insignificant_tokens(token_list, language='python'):

    filtered = []
    is_leading = True  # Флаг для отслеживания начала строки

    for token_type, token_value in token_list:
        # Всегда пропускаем комментарии
        if is_token_subtype(token_type, Token.Comment):
            continue
        if is_token_subtype(token_type, Token.Text.Whitespace) and token_value == '\n':
            continue
        # Обработка для Python
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

filepath = "add_function_end.md"
file_path = "expressions.py"
match, patch, source = load_code_from_markdown(filepath)
parsed_output = parse_match_string(match)
tr = transform_tuples(parsed_output, tokenize_code, "cpp")
tr3 = source_to_tokenList(file_path, tokenize_code, "python")


print("Match:", tr)
print("Patch:", patch)
print("Sourse:",  tr3)
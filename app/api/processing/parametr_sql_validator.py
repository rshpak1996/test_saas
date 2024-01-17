import re


def is_valid_sql(text):
    text = str(text)
    if not text:
        return False
    # Проверяем, что текст не содержит запрещенных SQL команд
    sql_regex = re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TABLE|VIEW)\b', re.IGNORECASE)
    if sql_regex.search(text):
        return False
    return True


if __name__ == '__main__':
    valid = is_valid_sql('SeLeCt')
    print(valid)
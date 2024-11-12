import re

def find_r(text, type):
    # Регулярное выражение для поиска email адресов
    email_pattern = r'[\n \"]([\w/+/.-]+@[\w\.-]+\w)'
    date_pattern = r'[\n ](\d{2}[\/-]\d{2}[\/-]\d{4})|(\d{4}[\/\.]\d{2}[\/\.]\d{2})|(\w+ \d{2}, \d{4})'

    
    # Находим все совпадения в тексте
    pattern = email_pattern if type == 'e' else date_pattern
    emails = re.findall(pattern, text)
    
    # Выводим результаты
    if emails:
        print("Найденные совпадения:")
        for i, email in enumerate(emails, 1):
            if isinstance(email, tuple):
                email = next(x for x in email if x)
            print(f"{i}. {email}")
    else:
        print("Совпадения не найдены")
    
    return emails


def get_text():
    with open('Regex home work.txt', 'r', encoding='utf-8') as file:
            return file.read()

def main():
    # Пример текста для поиска
    sample_text = get_text()
    
    # Вызов функции поиска
    found_emails = find_r(sample_text, 'e')
    found_emails = find_r(sample_text, 'd')


if __name__ == "__main__":
    main()
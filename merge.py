import csv
import re

# Пути к входным файлам
file_paths = ['contacts1.txt', 'contacts2.txt', 'contacts3.txt']

# Словарь для хранения уникальных контактов
contacts = {}

# Функция для очистки имени от неалфавитных символов (оставляем только буквы, цифры, пробел и запятые)
def clean_text(text):
    # Удалим все символы, кроме букв, цифр, пробелов, запятых и точки
    cleaned = re.sub(r'[^\w\s,.\-а-яА-ЯёЁa-zA-Z0-9]', '', text)
    return cleaned.strip()

# Чтение всех файлов
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                phone = row[0].strip()
                name = ",".join(row[1:]).strip()
                name = clean_text(name)
                contacts[phone] = name

# Запись в объединённый файл
with open('merged_contacts.txt', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for phone, name in contacts.items():
        writer.writerow([phone, name])

print("Файл 'merged_contacts' успешно создан.")



# Входной файл
input_file = 'merged_contacts.txt'

# Словари для хранения контактов
kazakh_contacts = {}
other_contacts = {}

# Функция очистки имени от эмодзи и лишнего
def clean_text(text):
    return re.sub(r'[^\w\s,.\-а-яА-ЯёЁa-zA-Z0-9]', '', text).strip()

# Чтение файла
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) >= 2:
            phone = row[0].strip()
            name = ",".join(row[1:]).strip()
            name = clean_text(name)

            if phone.startswith('77'):
                kazakh_contacts[phone] = name
            else:
                other_contacts[phone] = name

# Запись казахстанских номеров
with open('kazakh_contacts.txt', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for phone, name in kazakh_contacts.items():
        writer.writerow([phone, name])

# Запись остальных номеров
with open('other_contacts.txt', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for phone, name in other_contacts.items():
        writer.writerow([phone, name])

print("Готово! Созданы файлы 'kazakh_contacts' и 'other_contacts.csv'")

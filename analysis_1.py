from g4f.client import Client
import g4f
import os, datetime
import time
import random

promt_0 = (
    "Пожалуйста посмотри эту переписку и сделай короткий вывод что в итоге. "
    "Если человек интересуется обучением, то напиши новое сообщение для него чтоб возобновить беседу. "
    "Пиши на русском языке. Пиши 'Здравствуйте', не пиши имя и не используй имя в переписке. "
    "Не делай оценочные суждения. Перед новым сообщением сделай строку с символами +++, "
    "так я буду знать где новое сообщение."
)

# Поиск самой свежей папки
latest_folder_name = max(
    [d for d in os.listdir(".") if os.path.isdir(d) and d.startswith("chats_")],
    key=lambda name: datetime.datetime.strptime(name.replace("chats_", ""), "%Y-%m-%d_%H-%M"),
    default=None
)

if latest_folder_name:
    print("CHATS: ", latest_folder_name)
    analysis_folder_name = latest_folder_name.replace("chats_", "analysis_")
else:
    raise Exception("Папки chats_ не найдены.")

# Подготовка путей
analysis_folder_path = os.path.join(latest_folder_name, analysis_folder_name)
os.makedirs(analysis_folder_path, exist_ok=True)
print("ANALYSIS: ", analysis_folder_path)

input_path = latest_folder_name
output_folder = analysis_folder_path

# Сортировка файлов
files = os.listdir(input_path)
sorted_files = sorted(
    [f for f in files if f.endswith(".txt")],
    key=lambda name: int(name.split("_")[0])
)

client = Client()

# Обработка файлов
for filename in sorted_files:
    dest_path = os.path.join(output_folder, filename)
    if os.path.exists(dest_path):
        print(f"⏭ Пропущен (файл уже существует): {filename}")
        continue

    full_path = os.path.join(input_path, filename)

    while True:  # Цикл с повторной попыткой
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                dialog_text = file.read()

            response = client.chat.completions.create(
            model="gpt-4",
            provider=g4f.Provider.Blackbox,
            messages=[
                {"role": "user", "content": promt_0},
                {"role": "user", "content": dialog_text}
            ],
            web_search=False
        )

            result = response.choices[0].message.content

            print(f"\n🗂 Файл: {filename}")
            print(result)
            print("==================================")

            with open(dest_path, "w", encoding="utf-8") as out_file:
                out_file.write(result)

            time.sleep(20 + random.uniform(0, 5))
            break  # Успешно — выходим из while

        except Exception as e:
            print(f"❌ Ошибка при обработке {filename}: {e}")
            print("🔁 Повтор через 10 секунд...\n")
            time.sleep(10)

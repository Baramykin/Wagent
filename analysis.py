from g4f.client import Client
import g4f
import os, datetime
import time

promt_0 = "Пожалуйста посмотри эту переписку и сделай короткий вывод что в итоге. Если человек интересуется обучением, то напиши новое сообщение для него чтоб возобновить беседу. Пишина русском языке. Пиши Здравствуйте, не пиши имя и не используй имя в переписке. Не делай оценочные суждения. Пред новым сообщением сделай строку с символами +++, так я буду знать где новое сообщение."


latest_folder_name = max(
    [d for d in os.listdir(".") if os.path.isdir(d) and d.startswith("chats_")],
    key=lambda name: datetime.datetime.strptime(name.replace("chats_", ""), "%Y-%m-%d_%H-%M"),
    default=None
)

if latest_folder_name:
    print("CHATS: ", latest_folder_name)
    analysis_folder_name = latest_folder_name.replace("chats_", "analysis_")
else:
    print("Папки не найдены.")


analysis_folder_path = os.path.join(latest_folder_name, analysis_folder_name)
os.makedirs(analysis_folder_path, exist_ok=True)
print("ANALYSIS: ", analysis_folder_path)



input_path = latest_folder_name
output_folder = analysis_folder_path


files = os.listdir(input_path)
# Фильтруем только .txt файлы и сортируем по номеру в начале имени
sorted_files = sorted(
    [f for f in files if f.endswith(".txt")],
    key=lambda name: int(name.split("_")[0])
)
dest_path = os.path.join(output_folder, sorted_files[0])

client = Client()

# Читаем файлы по порядку
for filename in sorted_files:
    dest_path = os.path.join(output_folder, filename)
    if os.path.exists(dest_path):
        print(f"Пропущен (файл уже существует): {filename}")
        continue
    
    full_path = os.path.join(input_path, filename)
    with open(full_path, 'r', encoding='utf-8') as file:
        dialog_text = file.read()    
    
    response = client.chat.completions.create(
        provider=g4f.Provider.Blackbox,
        model="gpt-4",
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
    

    output_path = os.path.join(output_folder, filename)
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(result)

    time.sleep(20)


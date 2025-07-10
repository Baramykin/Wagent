from g4f.client import Client
import os

promt_0 = "Пожалуйста посмотри эту переписку и сделай короткий вывод что в итоге. "

promt_1 = "- Привет! Как дела? Дано тебя не видел! Пошли гулять!"


# promt = promt_0 + promt_1

client = Client()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": promt_0},
        {"role": "user", "content": promt_1}
    ],
    web_search=False
)


print(response.choices[0].message.content)
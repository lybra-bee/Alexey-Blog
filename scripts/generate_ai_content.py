import os
import requests
from datetime import datetime

HF_TOKEN = os.environ.get("HF_TOKEN")
POSTS_DIR = "../posts"

if not HF_TOKEN:
    print("HF_TOKEN не найден. Используется заглушка.")
    post_content = "# Hello AI Blog\nКонтент пока не генерируется."
else:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": "Напиши новый пост для моего портфолио-блога программиста и веб-дизайнера, сгенерируй краткий текст и идею картинки"}
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/gpt2",
        headers=headers,
        json=payload
    )
    if response.status_code == 200:
        post_content = f"# AI Post\n\n{response.json()[0]['generated_text']}"
    else:
        post_content = "# Ошибка генерации\nПроверь HF_TOKEN и модель."

# Создаём новый файл поста
date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = os.path.join(POSTS_DIR, f"{date_str}.md")
os.makedirs(POSTS_DIR, exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(post_content)

print(f"Пост сгенерирован: {filename}")

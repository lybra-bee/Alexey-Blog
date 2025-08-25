#!/usr/bin/env python3
import os, json, datetime, textwrap, base64, requests, random, re, pathlib

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(ROOT, ".."))
POSTS_DIR = os.path.join(SITE, "posts")
IMAGES_DIR = os.path.join(SITE, "images")

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

def slugify(s):
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")

def hf_text(prompt, model="mistralai/Mistral-7B-Instruct-v0.3"):
    if not HF_TOKEN:
        # fallback simple pseudo-generation
        return f"{prompt}\n\n(Демо-текст: добавь HF_TOKEN для реальной генерации)"
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 600, "temperature": 0.8}}
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    out = r.json()
    if isinstance(out, list) and out and "generated_text" in out[0]:
        return out[0]["generated_text"]
    if isinstance(out, dict) and "generated_text" in out:
        return out["generated_text"]
    # generic
    return str(out)

def hf_image(prompt, model="stabilityai/sd-turbo"):
    if not HF_TOKEN:
        return None
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "x-use-cache":"false"}
    payload = {"inputs": prompt}
    r = requests.post(url, headers=headers, json=payload, timeout=180)
    r.raise_for_status()
    # some models return base64 image as bytes; inference api may return raw bytes
    if r.headers.get("content-type", "").startswith("image/"):
        return r.content
    try:
        data = r.json()
        if isinstance(data, dict) and "generated_image" in data:
            return base64.b64decode(data["generated_image"])
    except Exception:
        pass
    return None

def main():
    topic = random.choice([
        "Советы по дизайну UI для AI-инструментов",
        "Интеграция FastAPI с генерацией видео и TTS",
        "Авто‑генерация контента в GitHub Actions",
        "Оптимизация клиента на Android для ИИ‑видео",
        "Сравнение бесплатных моделей ИИ для продакшена"
    ])
    title = f"{topic}: практическое руководство"
    date = str(datetime.date.today())
    cover_path = None
    img_prompt = f"clean modern illustration, minimal, for blog about: {topic}, high quality, 3D icon style"
    img = hf_image(img_prompt)
    if img:
        cover_name = f"{slugify(topic)}.png"
        cover_path = os.path.join(IMAGES_DIR, cover_name)
        with open(cover_path, "wb") as f:
            f.write(img)
        cover_url = f"/images/{cover_name}"
    else:
        cover_url = "/images/sample-cover.jpg"

    prompt = f"""
Ты — технический редактор. Напиши структурированную статью (600-900 слов) по теме: "{topic}".
Требования: введение, 3-5 разделов с подзаголовками, списки, минимальный код (если уместно), вывод, блок "Что дальше".
Пиши по-русски, делай акцент на практику и открытые бесплатные решения.
Заголовок статьи: "{title}".
"""
    body = hf_text(prompt)

    md = f"""---
title: "{title}"
date: {date}
tags: [ai, design, dev]
cover: {cover_url}
---

{body}
"""
    fname = f"{slugify(title)}.md"
    with open(os.path.join(POSTS_DIR, fname), "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    main()

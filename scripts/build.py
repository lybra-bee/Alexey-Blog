import os
import shutil
from jinja2 import Environment, FileSystemLoader
import markdown

POSTS_DIR = "./posts"
SITE_DIR = "./_site"
TEMPLATE_DIR = "./templates"

os.makedirs(SITE_DIR, exist_ok=True)

# Загружаем шаблон
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("index.html")

# Собираем все посты
posts_html = []
for filename in sorted(os.listdir(POSTS_DIR), reverse=True):
    if filename.endswith(".md"):
        with open(os.path.join(POSTS_DIR, filename), "r", encoding="utf-8") as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)
        posts_html.append(html_content)

# Генерируем главную страницу
output = template.render(posts=posts_html)
with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(output)

print("Сайт собран в:", SITE_DIR)

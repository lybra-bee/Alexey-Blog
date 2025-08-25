# Alexey — AI Engineer & Web Designer

Самообновляющийся портфолио‑блог с авто‑генерацией постов и деплоем на GitHub Pages.

## Быстрый старт

1. **Создай пустой репозиторий** на GitHub и включи Pages: Settings → Pages → Build and deployment → Source: *GitHub Actions*.
2. Скачай этот архив и залей содержимое в репозиторий.
3. (Опционально) Добавь секрет `HF_TOKEN` (Settings → Secrets → Actions → New repository secret), чтобы включить реальную генерацию текста/картинок через Hugging Face Inference API.
4. Сделай коммит — GitHub Actions соберёт сайт и задеплоит его на Pages.
5. Открой `/blog/`, там появится RSS‑лента `feed.json` и страницы постов.

## Структура
- `index.html` — главная, портфолио.
- `posts/*.md` — посты в Markdown с фронт‑маттером.
- `scripts/build.py` — сборка постов → HTML.
- `scripts/generate_ai_content.py` — генерация поста (работает без токена в демо‑режиме).
- `blog/` — собранные страницы блога и лента `feed.json`.
- `.github/workflows/publish.yml` — сборка по расписанию каждые 6 часов и деплой на Pages.

## Пользовательские настройки
Измени `config.json` (имя, тайтл, ссылки). Обнови карточки проектов на главной.

## Локальная сборка
```bash
python3 scripts/generate_ai_content.py   # опционально, создаст новый пост
python3 scripts/build.py                 # соберёт блог
# Открой index.html и /blog/index.html в браузере
```

## Примечание
- Для бесплатной генерации поставь публичные модели на Hugging Face и используй их в `generate_ai_content.py`. 
- Если токена нет — скрипт создаст демо‑пост без реального ИИ (чтобы пайплайн не падал).

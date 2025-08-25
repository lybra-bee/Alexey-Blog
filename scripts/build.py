#!/usr/bin/env python3
import os, json, re, pathlib, datetime, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(ROOT, ".."))
POSTS_DIR = os.path.join(SITE, "posts")
BLOG_DIR = os.path.join(SITE, "blog")

def parse_front_matter(md):
    fm = {}
    body = md
    if md.startswith("---"):
        parts = md.split("---", 2)
        if len(parts) >= 3:
            _, meta, body = parts
            for line in meta.strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body.strip()

def md_to_html(md):
    lines = md.splitlines()
    out = []
    for ln in lines:
        if ln.startswith("# "):
            out.append(f"<h1>{html.escape(ln[2:])}</h1>")
        elif ln.startswith("## "):
            out.append(f"<h2>{html.escape(ln[3:])}</h2>")
        elif ln.startswith("- "):
            out.append(f"<li>{html.escape(ln[2:])}</li>")
        elif ln.strip()== "":
            out.append("")
        else:
            out.append(f"<p>{html.escape(ln)}</p>")
    # Wrap list items
    html_str = "\n".join(out)
    html_str = re.sub(r"(?s)(?:\n)?(<li>.*?</li>)+", lambda m: f"<ul>{m.group(0)}</ul>", html_str)
    return html_str

def ensure(p):
    os.makedirs(p, exist_ok=True)

def main():
    ensure(BLOG_DIR)
    feed = []
    for fname in sorted(os.listdir(POSTS_DIR)):
        if not fname.endswith(".md"): 
            continue
        src = os.path.join(POSTS_DIR, fname)
        with open(src, "r", encoding="utf-8") as f:
            raw = f.read()
        fm, body = parse_front_matter(raw)
        title = fm.get("title", os.path.splitext(fname)[0])
        date = fm.get("date", str(datetime.date.today()))
        cover = fm.get("cover", "")
        slug = re.sub(r"[^a-z0-9-]+", "-", title.lower()).strip("-")
        excerpt = " ".join(body.split()[:32]) + ("..." if len(body.split())>32 else "")
        html_body = md_to_html(body)
        post_dir = os.path.join(BLOG_DIR, slug)
        ensure(post_dir)
        with open(os.path.join(post_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900">
  <main class="max-w-3xl mx-auto px-4 py-10">
    <a class="text-indigo-600" href="/blog/">← назад</a>
    <h1 class="text-3xl font-extrabold mt-4">{title}</h1>
    <p class="text-sm text-gray-500">{date}</p>
    {'<img class="mt-6 rounded-2xl shadow" src="'+cover+'" alt="cover">' if cover else ''}
    <article class="prose max-w-none mt-6">{html_body}</article>
  </main>
</body>
</html>""")
        feed.append({
            "title": title, "date": date, "slug": slug, "excerpt": excerpt, "cover": cover
        })
    with open(os.path.join(BLOG_DIR, "feed.json"), "w", encoding="utf-8") as f:
        json.dump(list(reversed(feed)), f, ensure_ascii=False, indent=2)
    # Blog index
    with open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write("""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Блог</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900">
  <main class="max-w-5xl mx-auto px-4 py-10">
    <h1 class="text-3xl font-extrabold">Блог</h1>
    <p class="text-gray-600 mt-2">Посты генерируются автоматически через GitHub Actions.</p>
    <div id="list" class="grid gap-4 mt-6"></div>
  </main>
  <script>
    fetch('/blog/feed.json').then(r=>r.json()).then(feed=>{
      const list = document.getElementById('list');
      list.innerHTML = feed.map(p=>`<a class="block p-4 bg-white rounded-2xl shadow hover:shadow-md transition" href="/blog/${p.slug}/">
        <h3 class="font-semibold">${p.title}</h3>
        <p class="text-sm text-gray-600 mt-1">${p.excerpt}</p>
        <p class="text-xs text-gray-400 mt-2">${p.date}</p>
      </a>`).join('');
    });
  </script>
</body>
</html>""")

if __name__ == "__main__":
    main()

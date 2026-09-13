#!/usr/bin/env python3
"""
build-og.py

Gera uma pagina estatica por post (posts/<slug>/index.html) com as tags
Open Graph e Twitter Card corretas (titulo, descricao, imagem, url), para
que o link tenha uma previa correta ao ser compartilhado em redes sociais.

O conteudo do post continua sendo carregado dinamicamente via JS
(post-loader.js), igual ao posts/post.html?slug=... de sempre -- este
script so cuida de gerar o <head> estatico que os crawlers de rede social
leem (eles nao executam JavaScript).

Uso:
    python3 scripts/build-og.py

Rode isso sempre que adicionar/editar um post em posts/index.json, antes
de dar commit + push.
"""

import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"
INDEX_JSON = POSTS_DIR / "index.json"
CONFIG_JSON = ROOT / "site.config.json"

PAGE_TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — {site_name}</title>
  <meta name="description" content="{description}" />

  <link rel="canonical" href="{url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="{site_name}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{url}" />
{og_image_tags}
  <!-- Twitter Card -->
  <meta name="twitter:card" content="{twitter_card}" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
{twitter_image_tag}
  <link rel="icon" href="data:," />
  <link rel="stylesheet" href="../../assets/css/style.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/tomorrow-night.min.css" />
</head>
<body>

  <header class="topbar">
    <a class="topbar__mark" href="../../index.html"><strong>obtuosa</strong>@logs:~$</a>
    <div class="topbar__right">
      <nav class="topbar__nav" aria-label="Navegação principal">
        <a href="../../index.html">home</a>
        <a href="../../whoami/index.html">whoami</a>
        <a href="../../manifesto/index.html">manifesto</a>
        <a href="../index.html" aria-current="page">posts</a>
      </nav>
      <button class="theme-toggle" type="button" data-theme-toggle>
        <svg class="theme-toggle__icon theme-toggle__icon--sun" viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="12" cy="12" r="5"/>
          <line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <svg class="theme-toggle__icon theme-toggle__icon--moon" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>
    </div>
  </header>

  <main class="shell">

    <nav class="crumb">
      <a class="crumb__back" href="../index.html">&larr; voltar para /posts</a>
    </nav>

    <article>
      <header class="post-header">
        <p class="post-header__meta" id="post-meta"></p>
        <h1 class="post-header__title" id="post-title">carregando registro&hellip;</h1>
        <p class="post-header__tags" id="post-tags"></p>
      </header>

      <div class="post-body prose" id="post-body"></div>
    </article>

  </main>

  <footer class="site-footer">
    <p class="site-footer__quote">See you space cowboy&hellip;</p>
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.1/marked.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>
  <script>
    marked.setOptions({{ gfm: true, breaks: false }});
    window.__POSTS_BASE__ = '../';
    window.__POST_SLUG__ = '{slug}';
  </script>
  <script src="../../assets/js/theme.js"></script>
  <script src="../../assets/js/post-loader.js"></script>
</body>
</html>
"""


def esc(value):
    return html.escape(value or "", quote=True)


def build():
    config = json.loads(CONFIG_JSON.read_text(encoding="utf-8"))
    base_url = config.get("baseUrl", "").rstrip("/")
    site_name = config.get("siteName", "Blog")
    default_image = config.get("defaultImage", "")

    if not base_url or "SEU-USUARIO" in base_url:
        print("[aviso] site.config.json ainda tem a baseUrl de exemplo.")
        print("        Edite baseUrl antes do deploy final, ou as tags")
        print("        og:image/og:url vao sair com esse placeholder.\n")

    posts = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    generated = 0

    for post in posts:
        slug = post["slug"]
        title = post.get("title", slug)
        description = post.get(
            "description",
            "Um registro em Obtuosa's Logs.",
        )
        image = post.get("image") or default_image

        post_dir = POSTS_DIR / slug
        post_dir.mkdir(parents=True, exist_ok=True)

        url = f"{base_url}/posts/{slug}/"

        if image:
            image_url = image if image.startswith("http") else f"{base_url}/posts/images/{image}"
            og_image_tags = (
                f'  <meta property="og:image" content="{esc(image_url)}" />\n'
                f'  <meta property="og:image:alt" content="{esc(title)}" />\n'
            )
            twitter_image_tag = f'  <meta name="twitter:image" content="{esc(image_url)}" />\n'
            twitter_card = "summary_large_image"
        else:
            og_image_tags = ""
            twitter_image_tag = ""
            twitter_card = "summary"

        html_out = PAGE_TEMPLATE.format(
            title=esc(title),
            description=esc(description),
            url=esc(url),
            site_name=esc(site_name),
            og_image_tags=og_image_tags,
            twitter_image_tag=twitter_image_tag,
            twitter_card=twitter_card,
            slug=slug,
        )

        (post_dir / "index.html").write_text(html_out, encoding="utf-8")
        generated += 1
        print(f"[ok] posts/{slug}/index.html")

    print(f"\n{generated} pagina(s) gerada(s) a partir de posts/index.json.")


if __name__ == "__main__":
    build()

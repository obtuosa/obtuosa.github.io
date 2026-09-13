# Obtuosa's Logs

Blog estático, minimalista, sem frameworks — HTML/CSS/JS puro, posts em Markdown,
pronto para o GitHub Pages.

## Estrutura (rotas)

Cada seção é uma pasta com seu próprio `index.html`, o que dá URLs limpas no
GitHub Pages (ex.: `seusite.com/whoami/`, sem precisar do `.html`).

```
.
├── index.html                # / — hub enxuto com links para as demais rotas
├── whoami/index.html         # /whoami — apresentação da autora
├── manifesto/index.html      # /manifesto — o manifesto
├── posts/
│   ├── index.html            # /posts — lista de artigos
│   ├── post.html             # leitor genérico de post (lê ?slug=, fallback)
│   ├── index.json            # metadados de cada post (title, date, tags, description, image)
│   ├── images/                # imagens de capa dos posts (og:image)
│   ├── *.md                  # conteúdo de cada post
│   └── <slug>/index.html     # gerado por scripts/build-og.py — NÃO editar à mão
├── scripts/
│   └── build-og.py           # gera posts/<slug>/index.html com as tags OG
├── site.config.json          # baseUrl usada nas tags og:url / og:image
└── assets/
    ├── css/style.css         # tema dark/light, tipografia, syntax highlight (compartilhado)
    └── js/
        ├── theme.js          # toggle dark/light com localStorage
        ├── posts-list.js     # monta a lista de artigos em /posts
        └── post-loader.js    # busca o .md pelo slug e renderiza
```

## Publicando um novo artigo

1. Escreva o texto em `posts/meu-artigo.md` (Markdown padrão: títulos, listas,
   tabelas, blockquotes, blocos de código com ```linguagem, imagens).
2. (Opcional) Coloque uma imagem de capa em `posts/images/meu-artigo.jpg`.
3. Adicione uma entrada em `posts/index.json`:

   ```json
   {
     "slug": "meu-artigo",
     "title": "Título do artigo",
     "date": "2026-09-10",
     "tags": ["appsec", "write-up"],
     "description": "Uma ou duas frases sobre o artigo (aparece na prévia do link).",
     "image": "meu-artigo.jpg"
   }
   ```

   `description` e `image` são opcionais — sem eles, a prévia sai só com título e
   descrição genérica, sem imagem.

4. Rode `python3 scripts/build-og.py`. Isso gera `posts/meu-artigo/index.html`
   com as tags Open Graph preenchidas (é o único passo de "build" do projeto —
   sem dependências além do Python 3 padrão).
5. Commit + push, incluindo a pasta `posts/meu-artigo/` gerada.

## Prévias em redes sociais (Open Graph)

O link `https://.../posts/meu-artigo/` (gerado no passo 4) é o que deve ser
compartilhado — ele já vem com `<meta property="og:...">` estáticas no HTML,
que é o que WhatsApp/Twitter/LinkedIn/Facebook leem para montar a prévia
(esses crawlers não executam JavaScript, por isso não dá pra confiar só no
`post.html?slug=...` dinâmico para isso).

Antes do primeiro deploy, edite `site.config.json` e troque `baseUrl` pela URL
real do seu GitHub Pages — sem isso, as tags saem com um domínio de exemplo.

## Deploy no GitHub Pages

1. Crie um repositório (ex.: `obtuosa.github.io` para domínio raiz, ou qualquer
   nome para um projeto em `usuario.github.io/repo`).
2. Edite `site.config.json` com a URL final e rode `python3 scripts/build-og.py`.
3. Suba todos os arquivos deste diretório para a branch `main`.
4. Em **Settings → Pages**, selecione a branch `main` e a pasta raiz (`/`).
5. O site fica disponível em `https://<usuario>.github.io/` (ou `/repo/`).

## Bibliotecas usadas (via CDN, sem build step)

- [marked.js](https://cdnjs.com/libraries/marked) — parser de Markdown
- [highlight.js](https://cdnjs.com/libraries/highlight.js) — syntax highlighting
  (Python e Bash já incluídos; adicione outros idiomas em `posts/post.html` se precisar)
- Google Fonts: `Source Serif 4` (corpo do texto) e `JetBrains Mono` (títulos,
  labels e blocos de código)

## Tema

O toggle no topo alterna entre:
- **Dark (padrão):** espaço profundo — fundo quase preto, texto cinza-claro,
  acentos em vermelho (Swordfish II) e dourado (jazz).
- **Light:** planeta desértico / papel de recompensa — fundo off-white/sépia,
  texto grafite, acentos em vermelho-terra e latão envelhecido.

A preferência é salva no `localStorage` do navegador de quem visita o site.

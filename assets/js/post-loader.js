(function () {
  var titleEl = document.getElementById('post-title');
  var metaEl = document.getElementById('post-meta');
  var tagsEl = document.getElementById('post-tags');
  var bodyEl = document.getElementById('post-body');
  if (!bodyEl) return;

  function formatDate(iso) {
    var d = new Date(iso + 'T00:00:00');
    if (isNaN(d)) return iso;
    return d.toLocaleDateString('pt-BR', { year: 'numeric', month: 'long', day: '2-digit' });
  }

  function params() {
    return new URLSearchParams(window.location.search);
  }

  // Páginas geradas por scripts/build-og.py (posts/<slug>/index.html) definem
  // window.__POST_SLUG__ e window.__POSTS_BASE__ antes deste script rodar.
  // O post.html?slug=... genérico continua funcionando como fallback.
  var base = window.__POSTS_BASE__ || '';
  var slug = window.__POST_SLUG__ || params().get('slug');

  if (!slug) {
    titleEl.textContent = 'Registro não encontrado';
    bodyEl.innerHTML = '<p>Nenhum artigo foi especificado na URL.</p>';
    return;
  }

  fetch(base + 'index.json', { cache: 'no-store' })
    .then(function (r) { return r.json(); })
    .then(function (posts) {
      var meta = posts.find(function (p) { return p.slug === slug; });
      if (!meta) throw new Error('not found');

      document.title = meta.title + ' — Obtuosa\u2019s Logs';
      titleEl.textContent = meta.title;
      metaEl.textContent = formatDate(meta.date);
      if (meta.tags && meta.tags.length) {
        tagsEl.textContent = meta.tags.join(' · ');
      }

      return fetch(base + meta.slug + '.md', { cache: 'no-store' });
    })
    .then(function (r) {
      if (!r.ok) throw new Error('missing markdown');
      return r.text();
    })
    .then(function (md) {
      bodyEl.innerHTML = marked.parse(md);
      if (window.hljs) {
        bodyEl.querySelectorAll('pre code').forEach(function (block) {
          hljs.highlightElement(block);
        });
      }
    })
    .catch(function () {
      titleEl.textContent = 'Registro não encontrado';
      bodyEl.innerHTML = '<p>Este artigo não existe ou foi removido da base de dados.</p>';
    });
})();

(function () {
  var listEl = document.getElementById('log-list');
  var emptyEl = document.getElementById('log-empty');
  if (!listEl) return;

  function formatDate(iso) {
    var d = new Date(iso + 'T00:00:00');
    if (isNaN(d)) return iso;
    return d.toLocaleDateString('pt-BR', { year: 'numeric', month: 'short', day: '2-digit' });
  }

  fetch('index.json', { cache: 'no-store' })
    .then(function (r) { return r.json(); })
    .then(function (posts) {
      if (!Array.isArray(posts) || posts.length === 0) {
        emptyEl.hidden = false;
        return;
      }

      posts
        .slice()
        .sort(function (a, b) { return new Date(b.date) - new Date(a.date); })
        .forEach(function (post) {
          var li = document.createElement('li');
          li.className = 'log__item';

          var a = document.createElement('a');
          a.className = 'log__link';
          a.href = post.slug + '/';

          var left = document.createElement('span');
          var title = document.createElement('span');
          title.className = 'log__link-title';
          title.textContent = post.title;
          left.appendChild(title);

          if (post.tags && post.tags.length) {
            var tags = document.createElement('span');
            tags.className = 'log__tags';
            tags.textContent = post.tags.join(' · ');
            left.appendChild(tags);
          }

          var meta = document.createElement('span');
          meta.className = 'log__meta';
          meta.textContent = formatDate(post.date);

          a.appendChild(left);
          a.appendChild(meta);
          li.appendChild(a);
          listEl.appendChild(li);
        });
    })
    .catch(function () {
      emptyEl.hidden = false;
      emptyEl.textContent = 'Não foi possível carregar os registros. Verifique index.json.';
    });
})();

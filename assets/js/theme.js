(function () {
  var STORAGE_KEY = 'obtuosa-theme';
  var root = document.documentElement;

  function applyTheme(theme) {
    if (theme === 'light') {
      root.setAttribute('data-theme', 'light');
    } else {
      root.removeAttribute('data-theme');
    }
  }

  function currentTheme() {
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches
      ? 'light'
      : 'dark';
  }

  // Aplica o tema o mais cedo possível para evitar flash de tema errado.
  applyTheme(currentTheme());

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.querySelector('[data-theme-toggle]');
    if (!btn) return;

    function ariaLabel(theme) {
      return theme === 'light' ? 'Mudar para modo noturno' : 'Mudar para modo diurno';
    }

    btn.setAttribute('aria-label', ariaLabel(currentTheme()));

    btn.addEventListener('click', function () {
      var next = currentTheme() === 'light' ? 'dark' : 'light';
      localStorage.setItem(STORAGE_KEY, next);
      applyTheme(next);
      btn.setAttribute('aria-label', ariaLabel(next));
    });
  });
})();

document.addEventListener('DOMContentLoaded', function () {
  const key = 'tt_theme';
  function current() { return localStorage.getItem(key) || 'dark'; }
  function apply(t) {
    if (t === 'light') document.documentElement.classList.add('light'); else document.documentElement.classList.remove('light');
    localStorage.setItem(key, t);
    const btn = document.getElementById('themeToggle');
    if (btn) btn.textContent = (t === 'light') ? 'Dark' : 'Light';
  }

  // add floating toggle button
  let btn = document.getElementById('themeToggle');
  if (!btn) {
    btn = document.createElement('button');
    btn.id = 'themeToggle';
    btn.className = 'btn btn-sm btn-outline-light theme-toggle';
    document.body.appendChild(btn);
  }

  apply(current());

  btn.addEventListener('click', function () {
    const next = (current() === 'light') ? 'dark' : 'light';
    apply(next);
  });
});

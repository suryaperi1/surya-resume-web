(function () {
  const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
  const panels = Array.from(document.querySelectorAll('[role="tabpanel"]'));

  function activateTab(tab) {
    const targetId = tab.getAttribute('aria-controls');

    tabs.forEach((t) => {
      const selected = t === tab;
      t.classList.toggle('active', selected);
      t.setAttribute('aria-selected', selected ? 'true' : 'false');
      t.tabIndex = selected ? 0 : -1;
    });

    /*panels.forEach((panel) => {
      const visible = panel.id === targetId;
      panel.classList.toggle('active', visible);
      panel.hidden = !visible;
    });*/

    panels.forEach((panel) => {
    const isActive = panel.id === targetId;
    panel.classList.toggle('active', isActive);

    if (isActive) {
      panel.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
      });
      }
    });

    history.replaceState(null, '', `#${targetId}`);
  }

  function tabFromHash() {
    const hash = location.hash.slice(1);
    return tabs.find((t) => t.getAttribute('aria-controls') === hash) || tabs[0];
  }

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => activateTab(tab));

    tab.addEventListener('keydown', (e) => {
      const index = tabs.indexOf(tab);
      let next = index;

      if (e.key === 'ArrowRight') next = (index + 1) % tabs.length;
      else if (e.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') next = 0;
      else if (e.key === 'End') next = tabs.length - 1;
      else return;

      e.preventDefault();
      tabs[next].focus();
      activateTab(tabs[next]);
    });
  });

  window.addEventListener('hashchange', () => activateTab(tabFromHash()));
  activateTab(tabFromHash());
})();

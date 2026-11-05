'use strict';
// Only non-sensitive concept IDs are persisted. The contact form stores nothing.
(() => {
  const studies = {
    '01': {title:'Room to Grow', image:'project-grid.svg', description:'An original plant-shop homepage concept exploring calm colors and a product-first layout.', decision:'Rounded image frames and a restrained green palette give three equal products a clear visual rhythm.', learning:'Using a responsive grid and a consistent spacing scale.'},
    '02': {title:'Small Notes', image:'project-notes.svg', description:'An original dashboard concept for collecting short ideas in a friendly, compact workspace.', decision:'A dark sidebar anchors the navigation while soft note colors separate content without heavy borders.', learning:'Creating a useful visual hierarchy with contrast, repetition, and grouping.'},
    '03': {title:'Steppe Atlas', image:'project-atlas.svg', description:'An original travel-page concept inspired by the open landscapes of Kazakhstan.', decision:'Layered vector mountains establish atmosphere while a large headline stays easy to read.', learning:'Balancing expressive illustrations with clear, readable interface content.'}
  };
  const storageKey = 'aisyn-portfolio-saved-v1';
  let saved = new Set();
  let storageAvailable = true;
  try {
    const parsed = JSON.parse(localStorage.getItem(storageKey) || '[]');
    if (Array.isArray(parsed)) saved = new Set(parsed.filter(id => Object.hasOwn(studies, id)));
  } catch { storageAvailable = false; }
  let activeFilter = 'all';
  function updateProjects() {
    document.querySelectorAll('[data-save]').forEach(button => {
      const selected = saved.has(button.dataset.save);
      button.setAttribute('aria-pressed', String(selected));
      button.setAttribute('aria-label', `${selected ? 'Unsave' : 'Save'} ${studies[button.dataset.save].title}`);
      button.textContent = selected ? '♥' : '♡';
    });
    const count = document.querySelector('#saved-count');
    if (count) count.textContent = saved.size;
    let visible = 0;
    document.querySelectorAll('#project-grid .project-item').forEach(card => {
      const show = activeFilter === 'all' || (activeFilter === 'saved' ? saved.has(card.dataset.id) : card.dataset.category === activeFilter);
      card.hidden = !show;
      if (show) visible++;
    });
    const result = document.querySelector('#result-count');
    if (result) result.textContent = `${visible} project${visible === 1 ? '' : 's'}`;
    const empty = document.querySelector('#empty-projects');
    if (empty) empty.hidden = visible !== 0;
    const storageStatus = document.querySelector('#storage-status');
    if (storageStatus && !storageAvailable) storageStatus.textContent = 'Browser storage is unavailable. Saved projects will only last for this page visit.';
  }
  document.querySelectorAll('[data-save]').forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.save;
    if (saved.has(id)) saved.delete(id); else saved.add(id);
    try { localStorage.setItem(storageKey, JSON.stringify([...saved])); } catch { storageAvailable = false; }
    updateProjects();
  }));
  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    activeFilter = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(filter => {
      const active = filter === button;
      filter.classList.toggle('active', active);
      filter.setAttribute('aria-pressed', String(active));
    });
    updateProjects();
  }));
  updateProjects();
  const modalElement = document.querySelector('#projectModal');
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement);
    let opener;
    document.querySelectorAll('[data-project]').forEach(button => button.addEventListener('click', () => {
      const project = studies[button.dataset.project];
      opener = button;
      document.querySelector('#project-title').textContent = project.title;
      document.querySelector('#project-description').textContent = project.description;
      document.querySelector('#project-decision').textContent = project.decision;
      document.querySelector('#project-learning').textContent = project.learning;
      const preview = document.querySelector('#project-preview');
      preview.src = `assets/images/${project.image}`;
      preview.alt = `${project.title} interface illustration`;
      modal.show();
    }));
    modalElement.addEventListener('hidden.bs.modal', () => opener?.focus());
  }
  // jQuery slide animation, with matching ARIA state and reduced-motion support.
  $('.journal-toggle').on('click', function () {
    const expanded = this.getAttribute('aria-expanded') === 'true';
    const panel = document.getElementById(this.getAttribute('aria-controls'));
    const $panel = $(panel);
    $panel.stop(true, true);
    this.setAttribute('aria-expanded', String(!expanded));
    $(this).find('.note-symbol').text(expanded ? '+' : '−');
    const duration = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 220;
    if (expanded) {
      $panel.slideUp(duration, () => { panel.hidden = true; });
    } else {
      panel.hidden = false;
      $panel.hide().slideDown(duration);
    }
  });
  const form = document.querySelector('#contact-form');
  if (form) {
    const fields = [...form.querySelectorAll('input, select, textarea')];
    const status = document.querySelector('#form-status');
    function validateField(field) {
      if (field.id === 'name' || field.id === 'message') {
        const minimum = field.id === 'name' ? 2 : 20;
        field.setCustomValidity(field.value.trim().length >= minimum ? '' : 'Please enter a longer value.');
      }
      if (form.classList.contains('was-validated')) field.setAttribute('aria-invalid', String(!field.validity.valid));
    }
    fields.forEach(field => field.addEventListener('input', () => {
      validateField(field);
      status.textContent = '';
      document.querySelector('#message-count').textContent = `${document.querySelector('#message').value.length} / 1000`;
    }));
    form.addEventListener('submit', event => {
      event.preventDefault();
      form.classList.add('was-validated');
      fields.forEach(validateField);
      if (!form.checkValidity()) {
        status.textContent = 'Please check the highlighted fields.';
        form.querySelector(':invalid').focus();
        return;
      }
      const message = document.createElement('p');
      message.className = 'form-status-message';
      message.textContent = `Thanks, ${document.querySelector('#name').value.trim()}! Your message passed validation. This was a local demo: nothing was sent or stored.`;
      status.replaceChildren(message);
      status.focus();
      form.reset();
      form.classList.remove('was-validated');
      fields.forEach(field => { field.removeAttribute('aria-invalid'); field.setCustomValidity(''); });
      document.querySelector('#message-count').textContent = '0 / 1000';
    });
  }
  const backTop = document.querySelector('#back-top');
  function updateScrollButton() { backTop.hidden = window.scrollY < 500; }
  window.addEventListener('scroll', updateScrollButton, {passive:true});
  updateScrollButton();
  backTop.addEventListener('click', () => { window.scrollTo({top:0, behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'}); document.querySelector('.brand').focus({preventScroll:true}); });
})();

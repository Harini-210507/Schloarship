// ===== Scholarship Application System — Main JS =====

// Hamburger menu toggle
document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.querySelector('.hamburger');
  const navLinks  = document.querySelector('.navbar-links');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => navLinks.classList.toggle('open'));
  }

  // Auto-dismiss alerts after 5 seconds
  document.querySelectorAll('.alert[data-auto-dismiss]').forEach(el => {
    setTimeout(() => el.style.display = 'none', 5000);
  });

  // Drag-and-drop upload zones
  document.querySelectorAll('.upload-zone').forEach(zone => {
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
    zone.addEventListener('drop', e => {
      e.preventDefault();
      zone.classList.remove('dragover');
      const input = zone.querySelector('input[type=file]');
      if (input && e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        input.dispatchEvent(new Event('change'));
      }
    });
    zone.addEventListener('click', () => zone.querySelector('input[type=file]')?.click());
  });

  // Show selected filename in upload zone
  document.querySelectorAll('.upload-zone input[type=file]').forEach(input => {
    input.addEventListener('change', () => {
      const zone     = input.closest('.upload-zone');
      const label    = zone?.querySelector('.upload-label');
      const existing = zone?.querySelector('.selected-file-name');
      if (existing) existing.remove();
      if (input.files.length && label) {
        const span = document.createElement('span');
        span.className = 'selected-file-name';
        span.style.cssText = 'display:block;font-size:.85rem;color:#2563eb;margin-top:.5rem;font-weight:500;';
        span.textContent = '📎 ' + input.files[0].name;
        label.after(span);
      }
    });
  });

  // Confirm before dangerous actions
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
  });

  // Tab switching
  document.querySelectorAll('.tabs .tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const group = tab.closest('.tab-group') || tab.parentElement;
      group.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const target = document.querySelector(tab.dataset.target);
      const panels = target?.parentElement?.querySelectorAll('.tab-panel');
      panels?.forEach(p => p.style.display = 'none');
      if (target) target.style.display = 'block';
    });
  });
});


// Minimal JS scaffold for dashboard interactions using Alpine-compatible patterns.
document.addEventListener('alpine:init', () => {
  // Global helper could be expanded later
});

// Toggle sidebar example (keeps markup simple; sidebar may listen for custom events)
window.addEventListener('toggle-sidebar', () => {
  document.querySelector('aside')?.classList.toggle('hidden');
});

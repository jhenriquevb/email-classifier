function copyToClipboard(elementId, button) {
  const element = document.getElementById(elementId);
  const text = element.innerText;

  navigator.clipboard.writeText(text).then(() => {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="bi bi-check me-1"></i>Copiado!';
    button.classList.add('copy-success');

    setTimeout(() => {
      button.innerHTML = originalText;
      button.classList.remove('copy-success');
    }, 2000);
  }).catch(err => {
    console.error('Erro ao copiar:', err);
  });
}

function toggleSection(sectionId) {
  const content = document.getElementById(sectionId);
  const icon = document.getElementById(sectionId + '-icon');
  
  if (content.classList.contains('collapsed')) {
    content.classList.remove('collapsed');
    icon.classList.remove('bi-chevron-right');
    icon.classList.add('bi-chevron-down');
  } else {
    content.classList.add('collapsed');
    icon.classList.remove('bi-chevron-down');
    icon.classList.add('bi-chevron-right');
  }
}

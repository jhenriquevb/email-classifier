document.addEventListener('DOMContentLoaded', function() {
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file');
  const selectFilesBtn = document.getElementById('select-files');
  const emailTextarea = document.getElementById('email_text');
  const submitBtn = document.getElementById('submit-btn');
  const form = document.getElementById('upload-form');
  const dropContent = document.getElementById('drop-content');
  const fileInfo = document.getElementById('file-info');
  const fileName = document.getElementById('file-name');
  const fileSize = document.getElementById('file-size');
  const removeFileBtn = document.getElementById('remove-file');
  const textAreaContainer = document.getElementById('text-area-container');

  let selectedFile = null;

  // Format file size
  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  // Show file info
  function showFileInfo(file) {
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    dropContent.classList.add('d-none');
    fileInfo.classList.remove('d-none');
    
    // Desativar seção de texto em vez de esconder
    const textColumn = document.querySelector('.text-column');
    textColumn.classList.add('disabled');
    
    submitBtn.disabled = false;
    dropZone.classList.remove('border-primary');
    dropZone.classList.add('border-success');
  }

  // Hide file info
  function hideFileInfo() {
    dropContent.classList.remove('d-none');
    fileInfo.classList.add('d-none');
    
    // Reativar seção de texto
    const textColumn = document.querySelector('.text-column');
    textColumn.classList.remove('disabled');
    
    dropZone.classList.remove('border-success', 'bg-success-subtle');
    dropZone.classList.add('border-primary');
    selectedFile = null;
    fileInput.value = '';
    checkSubmitButton();
  }

  // Check if submit should be enabled
  function checkSubmitButton() {
    submitBtn.disabled = !selectedFile && !emailTextarea.value.trim();
  }

  // Drag and drop events
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
  });

  function highlight(e) {
    dropZone.classList.add('bg-primary-subtle');
  }

  function unhighlight(e) {
    dropZone.classList.remove('bg-primary-subtle');
  }

  dropZone.addEventListener('drop', handleDrop, false);

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  function handleFiles(files) {
    if (files.length > 0) {
      const file = files[0];
      if (file.type === 'text/plain' || file.type === 'application/pdf' || 
          file.name.toLowerCase().endsWith('.txt') || file.name.toLowerCase().endsWith('.pdf')) {
        selectedFile = file;
        fileInput.files = files;
        showFileInfo(file);
      } else {
        alert('Por favor, selecione apenas arquivos .txt ou .pdf');
      }
    }
  }


  // File selection button
  selectFilesBtn.addEventListener('click', function() {
    fileInput.click();
  });

  fileInput.addEventListener('change', function() {
    if (this.files.length > 0) {
      selectedFile = this.files[0];
      showFileInfo(selectedFile);
      simulateProgress();
    }
  });

  // Remove file button
  removeFileBtn.addEventListener('click', hideFileInfo);

  // Text area changes
  emailTextarea.addEventListener('input', function() {
    const uploadColumn = document.querySelector('.upload-column');
    
    if (emailTextarea.value.trim()) {
      // Se há texto, desativar upload
      uploadColumn.classList.add('disabled');
    } else {
      // Se não há texto, reativar upload
      uploadColumn.classList.remove('disabled');
    }
    
    checkSubmitButton();
  });

  // Paste functionality
  dropZone.addEventListener('paste', function(e) {
    e.preventDefault();
    const items = e.clipboardData.items;
    
    for (let item of items) {
      if (item.kind === 'file') {
        const file = item.getAsFile();
        if (file.type === 'text/plain' || file.type === 'application/pdf') {
          selectedFile = file;
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(file);
          fileInput.files = dataTransfer.files;
          showFileInfo(file);
            return;
        }
      } else if (item.kind === 'string' && item.type === 'text/plain') {
        item.getAsString(function(text) {
          emailTextarea.value = text;
          checkSubmitButton();
        });
        return;
      }
    }
  });

  // Make drop zone focusable for paste
  dropZone.setAttribute('tabindex', '0');

  // Form submission
  form.addEventListener('submit', function(e) {
    const loadingOverlay = document.getElementById('loading-overlay');
    loadingOverlay.classList.add('show');
    
    submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Processando...';
    submitBtn.disabled = true;
  });

  // Initial check
  checkSubmitButton();
});
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const searchBtn = document.getElementById('searchBtn');
  const settingsToggle = document.getElementById('settingsToggle');
  const settingsArea = document.getElementById('settingsArea');
  const urlTemplateInput = document.getElementById('urlTemplate');
  const saveBtn = document.getElementById('saveBtn');
  const errorMsg = document.getElementById('errorMsg');

  const DEFAULT_TEMPLATE = 'https://github.com/search?q=%s';
  const STORAGE_KEY = 'searchUrlTemplate';

  // 1. 填充 i18n 文本
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const msg = chrome.i18n.getMessage(el.dataset.i18n);
    if (msg) el.textContent = msg;
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    const msg = chrome.i18n.getMessage(el.dataset.i18nPlaceholder);
    if (msg) el.placeholder = msg;
  });
  document.querySelectorAll('[data-i18n-title]').forEach((el) => {
    const msg = chrome.i18n.getMessage(el.dataset.i18nTitle);
    if (msg) el.title = msg;
  });

  // 2. 读取已保存的模板
  chrome.storage.local.get([STORAGE_KEY], (result) => {
    urlTemplateInput.value = result[STORAGE_KEY] || DEFAULT_TEMPLATE;
  });

  const showError = (key) => {
    errorMsg.textContent = chrome.i18n.getMessage(key);
    errorMsg.hidden = false;
  };
  const clearError = () => {
    errorMsg.textContent = '';
    errorMsg.hidden = true;
  };

  // 3. 模板校验：必须含 %s，且为 http/https
  const sanitizeTemplate = (raw) => {
    const t = (raw || '').trim();
    if (!t.includes('%s')) return null;
    let probe;
    try {
      probe = new URL(t.replace(/%s/g, 'test'));
    } catch {
      return null;
    }
    if (probe.protocol !== 'http:' && probe.protocol !== 'https:') return null;
    return t;
  };

  // 4. 执行搜索
  const performSearch = () => {
    const query = searchInput.value.trim();
    if (!query) return;

    const template = sanitizeTemplate(urlTemplateInput.value) || sanitizeTemplate(DEFAULT_TEMPLATE);
    if (!template) {
      showError('errorInvalidTemplate');
      settingsArea.classList.add('open');
      return;
    }
    clearError();

    const finalUrl = template.replace('%s', encodeURIComponent(query));
    chrome.tabs.create({ url: finalUrl });
    window.close();
  };

  searchBtn.addEventListener('click', performSearch);
  searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
  });

  // 5. 切换设置面板
  settingsToggle.addEventListener('click', () => {
    settingsArea.classList.toggle('open');
  });

  urlTemplateInput.addEventListener('input', clearError);

  // 6. 保存模板（含校验）
  saveBtn.addEventListener('click', () => {
    const template = sanitizeTemplate(urlTemplateInput.value);
    if (!template) {
      showError('errorInvalidTemplate');
      return;
    }
    clearError();

    chrome.storage.local.set({ [STORAGE_KEY]: template }, () => {
      saveBtn.textContent = chrome.i18n.getMessage('savedButton');
      saveBtn.style.backgroundColor = '#2da44e';
      setTimeout(() => {
        saveBtn.textContent = chrome.i18n.getMessage('saveButton');
        saveBtn.style.backgroundColor = '#0969da';
      }, 1500);
    });
  });
});
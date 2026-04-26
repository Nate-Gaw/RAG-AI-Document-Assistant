const scrollContainer = document.getElementById("scroll-container");
const navButtons = Array.from(document.querySelectorAll("[data-page]"));
const headerTitle = document.querySelector(".site-header__title");
const headerSubtitle = document.querySelector(".site-header__subtitle");

const STORAGE_KEY = "rag-ai-scroll-state";
const state = {
  page: resolvePageFromLocation(),
  activeStep: 0,
  renderToken: 0,
  scrollMemory: loadScrollMemory(),
  currentObserver: null,
  scrollListenerAttached: false,
  workspace: {
    messages: [],
    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    function clamp(value, min, max) {
      return Math.min(Math.max(value, min), max);
    }

    function getSteps(pageName) {
      return pageData[pageName]?.steps || [];
    }

    function getStep(pageName, index) {
      return getSteps(pageName)[index] || null;
    }

    function formatLabel(value) {
      return String(value).replace(/-/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
    }

    function renderTagList(tags = [], className = "tag-chip") {
      return tags.map((tag) => `<span class="${className}">${escapeHtml(tag)}</span>`).join("");
    }

    function buildStepTriggers(pageName) {
      return getSteps(pageName)
        .map(
          (step, index) => `
            <section class="step-trigger" data-step="${index}" aria-hidden="true">
              <span class="visually-hidden">${escapeHtml(step.eyebrow)} ${escapeHtml(step.title)}</span>
            </section>
          `
        )
        .join("");
    }

    function buildStepDots(pageName, activeIndex) {
      return getSteps(pageName)
        .map(
          (step, index) => `
            <button class="step-dot ${index === activeIndex ? "is-active" : ""}" type="button" data-step-nav="${index}" aria-label="Jump to ${escapeHtml(step.title)}">
              ${String(index + 1).padStart(2, "0")}
            </button>
          `
        )
        .join("");
    }

    function buildDirectionButtons(activeIndex, totalSteps) {
      const previousIndex = Math.max(activeIndex - 1, 0);
      const nextIndex = Math.min(activeIndex + 1, totalSteps - 1);
      return `
        <div class="step-actions">
          <button class="step-action" type="button" data-step-nav="${previousIndex}" ${activeIndex === 0 ? "disabled" : ""}>Previous Step</button>
          <button class="step-action step-action--primary" type="button" data-step-nav="${nextIndex}" ${activeIndex === totalSteps - 1 ? "disabled" : ""}>Next Step</button>
        </div>
      `;
    }

    function buildFlowPanel(pageName, step, activeIndex) {
      const steps = getSteps(pageName);
      const labels = steps.map((item) => item.key || item.title);
      return `
        <section class="flow-panel">
          <p class="flow-panel__eyebrow">${pageName === "home" ? "Story rail" : "Engineering rail"}</p>
          <div class="flow-panel__frame">
            <p class="flow-panel__label">Current step</p>
            <h4>${escapeHtml(step.stickyTitle)}</h4>
            <p>${escapeHtml(step.stickyCopy)}</p>
          </div>
          <div class="flow-panel__dots" aria-label="Step rail">
            ${labels
              .map(
                (label, index) => `
                  <button class="flow-chip ${index === activeIndex ? "is-active" : ""}" type="button" data-step-nav="${index}" aria-label="Jump to ${escapeHtml(formatLabel(label))}">
                    ${String(index + 1).padStart(2, "0")}
                  </button>
                `
              )
              .join("")}
          </div>
          ${buildDirectionButtons(activeIndex, steps.length)}
        </section>
      `;
    }

    function buildSlideMarkup(pageName, step, activeIndex) {
      const indexLabel = String(activeIndex + 1).padStart(2, "0");
      return `
        <div class="slide-shell">
          <section class="slide-copy">
            <p class="slide-kicker">${escapeHtml(step.eyebrow)}</p>
            <h2>${escapeHtml(step.title)}</h2>
            <p class="slide-lead">${escapeHtml(step.copy)}</p>
            <p class="slide-detail">${escapeHtml(step.detail)}</p>
            <div class="tag-row">
              ${renderTagList(step.tags || [])}
            </div>
            <div class="slide-meta">
              <span>Step ${indexLabel}</span>
              <span>${pageName === "home" ? "Home narrative" : "Technical narrative"}</span>
            </div>
          </section>

          <aside class="slide-visual">
            ${buildFlowPanel(pageName, step, activeIndex)}
          </aside>
        </div>
      `;
    }

    function buildPageShell(pageName) {
      if (pageName === "workspace") {
        const page = pageData.workspace;
        return `
          <section class="page workspace-page" data-page="workspace">
            <div class="workspace-shell">
              <section class="workspace-upload workspace-panel">
                <p class="page-kicker">Workspace</p>
                <h2>${escapeHtml(page.introTitle)}</h2>
                <p>${escapeHtml(page.introCopy)}</p>
                <form class="workspace-form" id="workspace-upload-form">
                  <input class="workspace-file" type="file" id="workspace-files" multiple accept=".pdf,.txt" />
                  <div class="workspace-actions">
                    <button class="primary-button" type="submit">Upload</button>
                    <button class="secondary-button" type="button" id="workspace-reset">Reset index</button>
                  </div>
                </form>
              </section>

              <section class="workspace-chat workspace-panel">
                <h4>Ask a question</h4>
                <form class="workspace-form" id="workspace-query-form">
                  <textarea class="workspace-input" id="workspace-question" placeholder="Ask about your documents..."></textarea>
                  <div class="workspace-actions">
                    <button class="primary-button" type="submit">Ask</button>
                  </div>
                </form>
                <div class="workspace-feed" id="workspace-feed" aria-live="polite"></div>
              </section>

              <aside class="workspace-sources workspace-panel">
                <h4>Sources</h4>
                <p>Retrieved passages appear here after a question is answered.</p>
                <div class="workspace-tag-row">
                  <span class="workspace-tag">UI only</span>
                  <span class="workspace-tag">Backend untouched</span>
                  <span class="workspace-tag">Same origin</span>
                </div>
              </aside>
            </div>
          </section>
        `;
      }

      const steps = getSteps(pageName);
      return `
        <section class="page page--${pageName}" data-page="${pageName}" style="--step-count:${steps.length};">
          <div class="scrolly-shell">
            <aside class="sticky-stage" id="sticky-stage" aria-live="polite">
              <div class="sticky-stage__inner" id="sticky-stage-inner"></div>
            </aside>

            <div class="step-track" aria-hidden="true">
              ${buildStepTriggers(pageName)}
            </div>
          </div>
        </section>
      `;
    }

    function renderWorkspaceFeed(message, role = "assistant") {
      const feed = document.getElementById("workspace-feed");
      if (!feed) return;

      const node = document.createElement("article");
      node.className = "feed-message";
      node.dataset.role = role;
      node.innerHTML = `
        <strong>${role === "user" ? "You" : "Assistant"}</strong>
        <p>${escapeHtml(message)}</p>
      `;
      feed.appendChild(node);
      feed.scrollTop = feed.scrollHeight;
    }

    function renderSources(sources = []) {
      const sourcePanel = document.querySelector(".workspace-sources");
      if (!sourcePanel) return;

      const existing = sourcePanel.querySelector(".source-list");
      if (existing) existing.remove();

      const list = document.createElement("ol");
      list.className = "source-list";
      list.innerHTML = sources.map((item) => `<li>${escapeHtml(item.text || "")}</li>`).join("");
      sourcePanel.appendChild(list);
    }

    function renderSticky(step, pageName, instant = false) {
      const sticky = document.getElementById("sticky-stage-inner");
      if (!sticky) return;

      const markup = buildSlideMarkup(pageName, step, state.activeStep);
      const token = ++state.renderToken;

      if (instant) {
        sticky.innerHTML = markup;
        return;
      }

      sticky.classList.add("is-transitioning");
      window.setTimeout(() => {
        if (token !== state.renderToken) return;
        sticky.innerHTML = markup;
        window.requestAnimationFrame(() => {
          sticky.classList.remove("is-transitioning");
        });
      }, 110);
    }

    function clearObserver() {
      if (!state.currentObserver) return;
      state.currentObserver.disconnect();
      state.currentObserver = null;
    }

    function setActiveSections(index) {
      Array.from(scrollContainer.querySelectorAll("[data-step]")).forEach((section) => {
        const active = Number(section.dataset.step) === index;
        section.classList.toggle("is-active", active);
        section.setAttribute("aria-current", active ? "step" : "false");
      });
    }

    function syncNavState(pageName) {
      navButtons.forEach((button) => {
        button.classList.toggle("is-active", button.dataset.page === pageName);
      });
    }

    function syncStepFromScroll(pageName) {
      const steps = getSteps(pageName);
      if (!steps.length) return;

      const height = Math.max(scrollContainer.clientHeight, 1);
      const nextIndex = clamp(Math.round(scrollContainer.scrollTop / height), 0, steps.length - 1);
      applyStep(nextIndex, { source: "scroll", pageName });
    }

    function scrollToStep(index) {
      const target = scrollContainer.querySelector(`[data-step="${index}"]`);
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }

    function applyStep(index, { source = "scroll", pageName = state.page, syncScroll = false } = {}) {
      const step = getStep(pageName, index);
      if (!step) return;

      const changed = index !== state.activeStep || pageName !== state.page;
      state.page = pageName;
      state.activeStep = index;
      document.documentElement.dataset.currentStep = String(index);
      setActiveSections(index);

      if (changed) {
        renderSticky(step, pageName, source === "init");
      }

      if (syncScroll) {
        scrollToStep(index);
      }
    }

    function setupScrollEngine() {
      clearObserver();

      const sections = Array.from(scrollContainer.querySelectorAll("[data-step]") );
      if (!sections.length) return;

      state.currentObserver = new IntersectionObserver(
        (entries) => {
          const visible = entries
            .filter((entry) => entry.isIntersecting)
            .sort((left, right) => right.intersectionRatio - left.intersectionRatio)[0];

          if (!visible) return;

          const nextIndex = Number(visible.target.dataset.step);
          if (Number.isNaN(nextIndex)) return;
          applyStep(nextIndex, { source: "scroll", pageName: state.page });
        },
        {
          root: scrollContainer,
          threshold: [0.4, 0.6, 0.8]
        }
      );

      sections.forEach((section) => state.currentObserver.observe(section));
    }

    function persistScroll() {
      state.scrollMemory[state.page] = scrollContainer.scrollTop;
      saveScrollMemory();
    }

    function restoreScroll(pageName) {
      scrollContainer.scrollTop = Number(state.scrollMemory[pageName] || 0);
    }

    function bindScrollTracking() {
      if (state.scrollListenerAttached) return;
      scrollContainer.addEventListener("scroll", persistScroll, { passive: true });
      scrollContainer.addEventListener("scroll", () => {
        if (state.page !== "workspace") {
          window.requestAnimationFrame(() => syncStepFromScroll(state.page));
        }
      }, { passive: true });
      state.scrollListenerAttached = true;
    }

    function bindNavigation() {
      navButtons.forEach((button) => {
        button.addEventListener("click", () => {
          showPage(button.dataset.page, true);
        });
      });

      scrollContainer.addEventListener("click", (event) => {
        const button = event.target.closest("[data-step-nav]");
        if (!button || button.disabled) return;

        const nextIndex = Number(button.dataset.stepNav);
        if (Number.isNaN(nextIndex)) return;

        applyStep(nextIndex, { source: "button", pageName: state.page, syncScroll: true });
      });

      window.addEventListener("popstate", () => {
        const nextPage = resolvePageFromLocation();
        showPage(nextPage, false);
      });
    }

    async function uploadDocuments(files) {
      const results = [];
      for (const file of files) {
        const formData = new FormData();
        formData.append("file", file);
        const response = await fetch("/upload", { method: "POST", body: formData });
        if (!response.ok) {
          const text = await response.text();
          throw new Error(text || `Upload failed for ${file.name}`);
        }
        results.push(await response.json());
      }
      return results;
    }

    async function resetIndex() {
      const response = await fetch("/reset", { method: "POST" });
      if (!response.ok) {
        throw new Error("Reset failed");
      }
    }

    async function askQuestion(question) {
      const response = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, top_k: 4 })
      });
      if (!response.ok) {
        throw new Error("Query failed");
      }
      return response.json();
    }

    function bindWorkspace() {
      const uploadForm = document.getElementById("workspace-upload-form");
      const queryForm = document.getElementById("workspace-query-form");
      const resetButton = document.getElementById("workspace-reset");
      const questionInput = document.getElementById("workspace-question");
      const fileInput = document.getElementById("workspace-files");

      if (uploadForm) {
        uploadForm.addEventListener("submit", async (event) => {
          event.preventDefault();
          const files = Array.from(fileInput.files || []);
          if (!files.length) {
            renderWorkspaceFeed("Choose one or more files before uploading.", "assistant");
            return;
          }

          renderWorkspaceFeed(`Uploading ${files.length} file(s)...`, "assistant");
          try {
            const responses = await uploadDocuments(files);
            const chunkCount = responses.reduce((total, item) => total + Number(item.chunks_added || 0), 0);
            renderWorkspaceFeed(`Indexed ${chunkCount} chunks.`, "assistant");
          } catch (error) {
            renderWorkspaceFeed(error.message, "assistant");
          }
        });
      }

      if (queryForm) {
        queryForm.addEventListener("submit", async (event) => {
          event.preventDefault();
          const question = questionInput.value.trim();
          if (!question) return;
          renderWorkspaceFeed(question, "user");
          questionInput.value = "";
          try {
            const data = await askQuestion(question);
            renderWorkspaceFeed(data.answer || "No answer returned.", "assistant");
            renderSources(data.sources || []);
          } catch (error) {
            renderWorkspaceFeed(error.message, "assistant");
          }
        });
      }

      if (resetButton) {
        resetButton.addEventListener("click", async () => {
          try {
            await resetIndex();
            const feed = document.getElementById("workspace-feed");
            if (feed) feed.innerHTML = "";
            renderWorkspaceFeed("Index cleared.", "assistant");
            renderSources([]);
          } catch (error) {
            renderWorkspaceFeed(error.message, "assistant");
          }
        });
      }
    }

    function showPage(pageName, pushState) {
      const nextPage = pageData[pageName] ? pageName : "home";
      state.page = nextPage;
      syncNavState(nextPage);

      if (pushState) {
        history.pushState({ page: nextPage }, "", pagePath(nextPage));
      }

      scrollContainer.innerHTML = buildPageShell(nextPage);
      bindScrollTracking();
      clearObserver();

      if (nextPage === "workspace") {
        bindWorkspace();
        restoreScroll(nextPage);
        return;
      }

      state.activeStep = 0;
      document.documentElement.dataset.currentStep = "0";
      setupScrollEngine();
      applyStep(0, { source: "init", pageName: nextPage });
      restoreScroll(nextPage);
      window.requestAnimationFrame(() => {
        syncStepFromScroll(nextPage);
      });
    }

    function init() {
      syncNavState(state.page);
      bindNavigation();
      showPage(state.page, false);
    }

    init();
  const sticky = document.getElementById("sticky-stage-inner");
  if (!sticky) return;

  const markup = pageName === "home" ? homeStickyContent(step) : technicalStickyContent(step);
  const token = ++state.renderToken;

  if (instant) {
    sticky.innerHTML = markup;
    return;
  }

  sticky.classList.add("is-transitioning");
  window.setTimeout(() => {
    if (token !== state.renderToken) return;
    sticky.innerHTML = markup;
    window.requestAnimationFrame(() => {
      sticky.classList.remove("is-transitioning");
    });
  }, 110);
}

function clearObserver() {
  if (state.currentObserver) {
    state.currentObserver.disconnect();
    state.currentObserver = null;
  }
}

function setActiveSections(index) {
  Array.from(scrollContainer.querySelectorAll("[data-step]")).forEach((section) => {
    const active = Number(section.dataset.step) === index;
    section.classList.toggle("is-active", active);
    section.classList.toggle("is-visible", active);
  });
}

function handleActiveStep(nextIndex) {
  const page = pageData[state.page];
  const step = page.steps[nextIndex];
  if (!step || nextIndex === state.activeStep) return;

  state.activeStep = nextIndex;
  document.documentElement.dataset.currentStep = String(nextIndex);
  setActiveSections(nextIndex);
  renderSticky(step, state.page);
}

function setupScrollEngine() {
  clearObserver();

  const sections = Array.from(scrollContainer.querySelectorAll("[data-step]"));
  if (!sections.length) return;

  state.currentObserver = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((left, right) => right.intersectionRatio - left.intersectionRatio)[0];

      if (!visible) return;

      const nextIndex = Number(visible.target.dataset.step);
      if (Number.isNaN(nextIndex)) return;
      handleActiveStep(nextIndex);
    },
    {
      root: scrollContainer,
      threshold: [0.35, 0.55, 0.75]
    }
  );

  sections.forEach((section) => state.currentObserver.observe(section));
}

function persistScroll() {
  state.scrollMemory[state.page] = scrollContainer.scrollTop;
  saveScrollMemory();
}

function restoreScroll(pageName) {
  const saved = Number(state.scrollMemory[pageName] || 0);
  scrollContainer.scrollTop = saved;
}

function syncHeader(pageName) {
  const page = pageData[pageName];
  if (headerTitle) headerTitle.textContent = page.title;
  if (headerSubtitle) headerSubtitle.textContent = page.subtitle;
  navButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.page === pageName);
  });
}

function bindScrollTracking() {
  if (state.scrollListenerAttached) return;
  scrollContainer.addEventListener("scroll", persistScroll, { passive: true });
  state.scrollListenerAttached = true;
}

function bindNavigation() {
  navButtons.forEach((button) => {
    button.addEventListener("click", () => {
      showPage(button.dataset.page, true);
    });
  });

  window.addEventListener("popstate", () => {
    const nextPage = resolvePageFromLocation();
    showPage(nextPage, false);
  });
}

async function uploadDocuments(files) {
  const results = [];
  for (const file of files) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });
    if (!response.ok) {
      const text = await response.text();
      throw new Error(text || `Upload failed for ${file.name}`);
    }
    results.push(await response.json());
  }
  return results;
}

async function resetIndex() {
  const response = await fetch("/reset", { method: "POST" });
  if (!response.ok) {
    throw new Error("Reset failed");
  }
}

async function askQuestion(question) {
  const response = await fetch("/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question, top_k: 4 })
  });
  if (!response.ok) {
    throw new Error("Query failed");
  }
  return response.json();
}

function bindWorkspace() {
  const uploadForm = document.getElementById("workspace-upload-form");
  const queryForm = document.getElementById("workspace-query-form");
  const resetButton = document.getElementById("workspace-reset");
  const questionInput = document.getElementById("workspace-question");
  const fileInput = document.getElementById("workspace-files");

  if (uploadForm) {
    uploadForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const files = Array.from(fileInput.files || []);
      if (!files.length) {
        renderWorkspaceFeed("Choose one or more files before uploading.", "assistant");
        return;
      }

      renderWorkspaceFeed(`Uploading ${files.length} file(s)...`, "assistant");
      try {
        const responses = await uploadDocuments(files);
        renderWorkspaceFeed(`Indexed ${responses.reduce((total, item) => total + Number(item.chunks_added || 0), 0)} chunks.`, "assistant");
      } catch (error) {
        renderWorkspaceFeed(error.message, "assistant");
      }
    });
  }

  if (queryForm) {
    queryForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const question = questionInput.value.trim();
      if (!question) return;
      renderWorkspaceFeed(question, "user");
      questionInput.value = "";
      try {
        const data = await askQuestion(question);
        renderWorkspaceFeed(data.answer || "No answer returned.", "assistant");
        renderSources(data.sources || []);
      } catch (error) {
        renderWorkspaceFeed(error.message, "assistant");
      }
    });
  }

  if (resetButton) {
    resetButton.addEventListener("click", async () => {
      try {
        await resetIndex();
        const feed = document.getElementById("workspace-feed");
        if (feed) feed.innerHTML = "";
        renderWorkspaceFeed("Index cleared.", "assistant");
        renderSources([]);
      } catch (error) {
        renderWorkspaceFeed(error.message, "assistant");
      }
    });
  }
}

function showPage(pageName, pushState) {
  const nextPage = pageData[pageName] ? pageName : "home";
  state.page = nextPage;
  syncHeader(nextPage);

  if (pushState) {
    history.pushState({ page: nextPage }, "", pagePath(nextPage));
  }

  scrollContainer.innerHTML = renderPageShell(nextPage);
  bindScrollTracking();
  clearObserver();

  if (nextPage === "workspace") {
    bindWorkspace();
    restoreScroll(nextPage);
    return;
  }

  state.activeStep = 0;
  document.documentElement.dataset.currentStep = "0";
  setupScrollEngine();
  renderSticky(pageData[nextPage].steps[0], nextPage, true);
  requestAnimationFrame(() => {
    setActiveSections(0);
    restoreScroll(nextPage);
  });
}

function init() {
  syncHeader(state.page);
  bindNavigation();
  showPage(state.page, false);
}

init();

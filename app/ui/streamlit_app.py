import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="RAG AI Document Assistant", page_icon="📄", layout="wide")

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

base_bg = "#0b0f14"
panel_bg = "#111821"
text_color = "#e6e8ec"
accent = "#2dd4bf"
brand_accent = "#7dd3fc"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@400;600;700&display=swap');

:root {{
  --bg: {base_bg};
  --panel: {panel_bg};
  --text: {text_color};
  --accent: {accent};
  --brand: {brand_accent};
  --muted: rgba(230,232,236,0.6);
  --soft: rgba(255,255,255,0.06);
  --edge: rgba(255,255,255,0.08);
}}

* {{
  box-sizing: border-box;
}}

html, body, [class*="css"] {{
  font-family: 'IBM Plex Sans', system-ui, -apple-system, sans-serif;
  color: var(--text);
  height: 100%;
  overflow: hidden;
}}

.stApp {{
  background: radial-gradient(1200px 600px at 10% -10%, rgba(45,212,191,0.12), transparent 55%),
    radial-gradient(900px 500px at 90% -20%, rgba(56,189,248,0.08), transparent 55%),
    var(--bg);
}}

section[data-testid="stSidebar"] {{
  width: 280px;
  min-width: 280px;
  background: #0b121a;
  border-right: 1px solid var(--edge);
}}

section[data-testid="stSidebar"] > div:first-child {{
  padding-top: 1.1rem;
}}

section[data-testid="stAppViewContainer"] {{
  height: 100vh;
  overflow: hidden;
}}

section.main > div.block-container {{
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 18px 28px 28px;
  overflow: hidden;
}}

.header-title {{
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 0.2rem;
}}

.header-subtitle {{
  font-size: 0.98rem;
  color: var(--muted);
  margin-bottom: 0.8rem;
}}

.header-divider {{
  height: 1px;
  background: rgba(255,255,255,0.08);
  margin: 0.35rem 0 1rem;
}}

.panel {{
  background: var(--panel);
  border: 1px solid var(--edge);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}}

.panel-title {{
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 0.35rem;
}}

.panel-subtitle {{
  color: var(--muted);
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
}}

.nav-brand {{
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 1.05rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--brand);
}}

.nav-brand span {
  color: var(--text);
  margin-left: 0.35rem;
  letter-spacing: 0.04em;
}

.topbar {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border: 1px solid var(--edge);
  border-radius: 14px;
  background: rgba(255,255,255,0.02);
  box-shadow: 0 14px 30px rgba(0,0,0,0.25);
}}

.topbar-sep {{
  height: 1px;
  background: rgba(255,255,255,0.08);
  margin: 8px 0 18px;
}}

.sidebar-section {{
  font-size: 0.78rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0.9rem 0 0.5rem;
}}

.file-list {{
  max-height: 260px;
  overflow-y: auto;
  padding-right: 4px;
}}

.stButton button {
  background: rgba(255,255,255,0.02);
  color: var(--text);
  border-radius: 999px;
  border: 1px solid var(--edge);
  padding: 0.45rem 1.05rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.stButton button:hover {
  border-color: rgba(125,211,252,0.5);
  color: var(--brand);
}

.stButton button[kind="primary"] {
  background: linear-gradient(120deg, rgba(45,212,191,0.4), rgba(125,211,252,0.25));
  border-color: rgba(45,212,191,0.6);
  color: var(--text);
  box-shadow: 0 10px 24px rgba(45,212,191,0.22);
}

.stTextArea textarea {{
  min-height: 54px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--edge);
  color: var(--text);
}}

.info-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-top: 12px;
}}

.info-card {{
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--edge);
  border-radius: 14px;
  padding: 14px 16px;
}}

.info-card h4 {{
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 1rem;
  margin: 0 0 6px;
}}

.info-card p {{
  color: var(--muted);
  font-size: 0.9rem;
  margin: 0;
}}

[data-testid="stChatMessage"] {{
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--edge);
  border-radius: 12px;
  padding: 10px 12px;
}}

[data-testid="stChatMessage"] p {{
  margin-bottom: 0.2rem;
}}

@media (max-width: 900px) {{
  section.main > div.block-container {{
    padding: 16px 16px 24px;
  }}
}}
</style>
""",
    unsafe_allow_html=True,
)

if "files" not in st.session_state:
    st.session_state.files = {}
if "upload_signature" not in st.session_state:
    st.session_state.upload_signature = None
if "messages" not in st.session_state:
  st.session_state.messages = []
if "page" not in st.session_state:
  st.session_state.page = "Home"

nav_left, nav_right = st.columns([2, 1])
with nav_left:
  st.markdown(
    '<div class="topbar"><div class="nav-brand">RAG<span>AI</span></div></div>',
    unsafe_allow_html=True,
  )
with nav_right:
  nav_col1, nav_col2 = st.columns(2)
  with nav_col1:
    if st.button(
      "Home",
      key="nav-home",
      type="primary" if st.session_state.page == "Home" else "secondary",
    ):
      st.session_state.page = "Home"
  with nav_col2:
    if st.button(
      "Workspace",
      key="nav-workspace",
      type="primary" if st.session_state.page == "Workspace" else "secondary",
    ):
      st.session_state.page = "Workspace"
page = st.session_state.page
st.markdown('<div class="topbar-sep"></div>', unsafe_allow_html=True)


def _reset_store() -> None:
    try:
        reset_resp = requests.post(f"{backend_url}/reset", timeout=30)
        reset_resp.raise_for_status()
    except requests.RequestException as exc:
        st.error(f"Failed to reset index: {exc}")
        st.stop()


def _upload_documents(files: list[st.runtime.uploaded_file_manager.UploadedFile]) -> None:
    _reset_store()
    for upload in files:
        payload = {"file": (upload.name, upload.getvalue())}
        try:
            resp = requests.post(f"{backend_url}/upload", files=payload, timeout=120)
            resp.raise_for_status()
        except requests.RequestException as exc:
            st.error(f"Upload failed for {upload.name}: {exc}")


def _signature_for(uploads: list[st.runtime.uploaded_file_manager.UploadedFile]) -> tuple[str, ...]:
    return tuple(sorted(f"{upload.name}:{upload.size}" for upload in uploads))


def _ask_backend(question: str) -> tuple[str, list[dict[str, str | float]]]:
    payload = {"question": question, "top_k": 4}
    try:
        resp = requests.post(f"{backend_url}/query", json=payload, timeout=120)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return f"Query failed: {exc}", []
    data = resp.json()
    return data.get("answer", ""), data.get("sources", [])


if page == "Workspace":
  with st.sidebar:
    st.markdown("### Documents")
    st.markdown('<div class="sidebar-section">Upload</div>', unsafe_allow_html=True)
    uploads = st.file_uploader(
      "Upload Document",
      type=["pdf", "txt"],
      accept_multiple_files=True,
      label_visibility="collapsed",
    )

    signature = _signature_for(uploads) if uploads else tuple()
    if st.session_state.upload_signature != signature:
      if uploads:
        st.session_state.files = {
          upload.name: {"data": upload.getvalue(), "type": upload.type}
          for upload in uploads
        }
        with st.spinner("Processing and indexing..."):
          _upload_documents(uploads)
      else:
        if st.session_state.files:
          _reset_store()
        st.session_state.files = {}
      st.session_state.messages = []
      st.session_state.upload_signature = signature

    st.markdown('<div class="sidebar-section">Documents</div>', unsafe_allow_html=True)
    if st.session_state.files:
      st.caption(f"{len(st.session_state.files)} document(s) uploaded.")
    else:
      st.caption("Upload documents to begin.")

if page == "Home":
    st.markdown('<div class="header-title">RAG AI Document Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="header-subtitle">A focused workspace for asking questions against your own documents.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">At a glance</div>', unsafe_allow_html=True)
    st.markdown(
        "Upload PDFs or text files, ask questions in natural language, and review the supporting "
        "chunks under Sources. Answers are summarized for clarity, not copied verbatim.",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
<div class="info-grid">
  <div class="info-card">
    <h4>What it does</h4>
    <p>Indexes your documents and answers questions with retrieved context.</p>
  </div>
  <div class="info-card">
    <h4>How it works</h4>
    <p>Parse → chunk → embed → retrieve → summarize with a language model.</p>
  </div>
  <div class="info-card">
    <h4>How to use</h4>
    <p>Open Workspace, upload files, then ask questions and review Sources.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="header-title">RAG AI Document Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="header-subtitle">Curated document previews with a focused, readable chat experience.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Preview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-subtitle">Scan the document stack before asking questions.</div>',
        unsafe_allow_html=True,
    )
    if st.session_state.files:
        for name, file_info in st.session_state.files.items():
            with st.expander(name, expanded=False):
                if file_info.get("type") == "text/plain":
                    preview_text = file_info["data"].decode("utf-8", errors="ignore")
                    st.text_area(
                        f"Preview: {name}",
                        value=preview_text,
                        height=220,
                        label_visibility="collapsed",
                    )
                else:
                    st.info("PDF preview not available. The file is indexed.")
    else:
        st.caption("Upload documents to preview their contents.")
    st.markdown('<div class="panel-title">Chat</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-subtitle">Ask once. We answer with a summary and cite sources.</div>',
        unsafe_allow_html=True,
    )
    if not st.session_state.messages:
        st.caption("Ask a question about your uploaded documents.")
    for message in st.session_state.messages:
        role = message.get("role", "assistant")
        content = message.get("content", "")
        sources = message.get("sources", [])
        with st.chat_message(role):
            st.markdown(content)
            if sources and role == "assistant":
                with st.expander("Sources", expanded=False):
                    for idx, item in enumerate(sources):
                        st.markdown(f"{idx + 1}. {item.get('text', '')}")
    st.markdown("</div>", unsafe_allow_html=True)

    prompt = st.chat_input("Ask a question about your documents")
    if prompt:
        if not st.session_state.files:
            st.warning("Upload a document before asking a question.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Thinking..."):
                answer, sources = _ask_backend(prompt)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": sources}
            )
        st.rerun()


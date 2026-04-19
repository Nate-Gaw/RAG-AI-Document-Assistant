import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="RAG AI Document Assistant", page_icon="📄", layout="wide")

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

base_bg = "#0f172a"
panel_bg = "#111827"
text_color = "#e5e7eb"
accent = "#14b8a6"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root {{
  --bg: {base_bg};
  --panel: {panel_bg};
  --text: {text_color};
  --accent: {accent};
}}

* {{
  box-sizing: border-box;
}}

html, body, [class*="css"] {{
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: var(--text);
  height: 100%;
  overflow: hidden;
}}

.stApp {{
  background: var(--bg);
}}

section[data-testid="stSidebar"] {{
  width: 280px;
  min-width: 280px;
  background: #0b1220;
  border-right: 1px solid rgba(255,255,255,0.08);
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
  padding: 16px 24px;
  overflow: hidden;
}}

.header-title {{
  font-size: 1.6rem;
  font-weight: 700;
  margin-bottom: 0.1rem;
}}

.header-subtitle {{
  font-size: 0.95rem;
  opacity: 0.7;
  margin-bottom: 0.6rem;
}}

.header-divider {{
  height: 1px;
  background: rgba(255,255,255,0.08);
  margin: 0.35rem 0 0.8rem;
}}

.panel {{
  background: var(--panel);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 12px 14px;
}}

.sidebar-section {{
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.7;
  margin: 0.9rem 0 0.5rem;
}}

.file-list {{
  max-height: 260px;
  overflow-y: auto;
  padding-right: 4px;
}}

[data-testid="stRadio"] label {{
  background: transparent;
  border-radius: 8px;
  padding: 6px 8px;
  margin-bottom: 4px;
}}

[data-testid="stRadio"] label:hover {{
  background: rgba(148,163,184,0.12);
}}

[data-testid="stRadio"] input:checked + div {{
  background: rgba(20,184,166,0.18);
  border-radius: 8px;
  padding: 6px 8px;
}}

.stButton button {{
  background: var(--accent);
  color: #0b1220;
  border-radius: 10px;
  border: none;
  padding: 0.5rem 0.9rem;
}}

.stTextArea textarea {{
  min-height: 54px;
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

st.markdown('<div class="header-title">RAG AI Document Assistant</div>', unsafe_allow_html=True)
st.markdown(
  '<div class="header-subtitle">Preview all documents and chat with the collection.</div>',
  unsafe_allow_html=True,
)
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("#### Preview")
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
st.markdown("#### Chat")
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


import html
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
  font-size: 1.7rem;
  font-weight: 700;
  margin-bottom: 0.1rem;
}}

.header-subtitle {{
  font-size: 0.95rem;
  opacity: 0.7;
  margin-bottom: 0.4rem;
}}

.header-divider {{
  height: 1px;
  background: rgba(255,255,255,0.08);
  margin: 0.35rem 0 0.7rem;
}}

.chat-shell {{
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  background: var(--panel);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 12px;
}}

.chat-messages {{
  flex: 1;
  overflow-y: auto;
  padding: 8px 12px 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
}}

.message {{
  max-width: 70%;
  padding: 10px 12px;
  border-radius: 14px;
  line-height: 1.4;
  border: 1px solid rgba(255,255,255,0.08);
}}

.message.user {{
  align-self: flex-end;
  background: rgba(30,41,59,0.8);
}}

.message.ai {{
  align-self: flex-start;
  background: rgba(15,23,42,0.8);
}}

.input-bar {{
  display: flex;
  gap: 12px;
  align-items: flex-end;
  margin: 10px auto 0;
  padding: 10px 12px;
  width: 100%;
  max-width: 900px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.08);
  background: #0b1220;
}}

.empty-state {{
  color: rgba(226,232,240,0.7);
  font-size: 0.92rem;
  padding: 0.5rem 0.4rem;
}}

.sidebar-section {{
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.7;
  margin: 0.6rem 0 0.4rem;
}}

.upload-box {{
  border: 1px dashed rgba(255,255,255,0.2);
  border-radius: 12px;
  padding: 10px;
}}

.file-list {{
  max-height: 260px;
  overflow-y: auto;
  padding-right: 4px;
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

if "chat" not in st.session_state:
    st.session_state.chat = []
if "files" not in st.session_state:
  st.session_state.files = {}
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None
if "upload_signature" not in st.session_state:
    st.session_state.upload_signature = None


def _escape(text: str) -> str:
    return html.escape(text)


def _reset_store() -> None:
    reset_resp = requests.post(f"{backend_url}/reset", timeout=30)
    if reset_resp.status_code != 200:
        st.error("Failed to reset index before upload.")
        st.stop()


def _upload_documents(files: list[st.runtime.uploaded_file_manager.UploadedFile]) -> None:
  _reset_store()

  for upload in files:
    payload = {"file": (upload.name, upload.getvalue())}
    resp = requests.post(f"{backend_url}/upload", files=payload, timeout=120)
    if resp.status_code != 200:
      st.error(resp.json().get("detail", f"Upload failed for {upload.name}."))


with st.sidebar:
    st.markdown("### Documents")
    st.markdown('<div class="sidebar-section">Upload</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploads = st.file_uploader(
        "Upload Document",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    signature = tuple(sorted(f"{u.name}:{u.size}" for u in uploads)) if uploads else tuple()
    if st.session_state.upload_signature != signature:
        if uploads:
            st.session_state.files = {
                upload.name: {"data": upload.getvalue(), "type": upload.type}
                for upload in uploads
            }
            with st.spinner("Processing and indexing..."):
                _upload_documents(uploads)
            st.session_state.selected_file = uploads[0].name
        else:
            if st.session_state.files:
                _reset_store()
            st.session_state.files = {}
            st.session_state.selected_file = None
        st.session_state.upload_signature = signature

    st.markdown('<div class="sidebar-section">Documents</div>', unsafe_allow_html=True)
    if st.session_state.files:
        with st.container():
            st.markdown('<div class="file-list">', unsafe_allow_html=True)
            st.session_state.selected_file = st.radio(
                "Select a file",
                list(st.session_state.files.keys()),
                index=list(st.session_state.files.keys()).index(st.session_state.selected_file)
                if st.session_state.selected_file in st.session_state.files
                else 0,
                label_visibility="collapsed",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">Preview</div>', unsafe_allow_html=True)
        selected = st.session_state.files.get(st.session_state.selected_file)
        if selected:
            if selected["type"] == "text/plain":
                preview_text = selected["data"].decode("utf-8", errors="ignore")
                st.text_area("Preview", value=preview_text, height=240, label_visibility="collapsed")
            else:
                st.info("PDF preview not available. The file is indexed for Q&A.")
    else:
        st.caption("Upload a document and ask a question to begin.")

st.markdown('<div class="header-title">RAG AI Document Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="header-subtitle">Upload documents, preview content, and chat with your files.</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
if not st.session_state.chat:
    st.markdown(
        '<div class="empty-state">Upload a document and ask a question to begin.</div>',
        unsafe_allow_html=True,
    )

for message in st.session_state.chat:
    role = message.get("role", "assistant")
    content = _escape(message.get("content", ""))
    role_class = "user" if role == "user" else "ai"
    st.markdown(f'<div class="message {role_class}">{content}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown('<div class="input-bar">', unsafe_allow_html=True)
with st.form("chat_input", clear_on_submit=True):
    input_col, button_col = st.columns([6, 1])
    with input_col:
        question = st.text_area(
            "Ask a question",
            placeholder="Ask a question about your documents...",
            height=54,
            label_visibility="collapsed",
        )
    with button_col:
        submitted = st.form_submit_button("Send")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if submitted and question.strip():
    if not st.session_state.files:
        st.warning("Please upload a document first")
    else:
        st.session_state.chat.append({"role": "user", "content": question.strip()})
        with st.spinner("Retrieving context and generating answer..."):
            payload = {"question": question.strip(), "top_k": 4}
            resp = requests.post(f"{backend_url}/query", json=payload, timeout=120)
            if resp.status_code != 200:
                answer_text = resp.json().get("detail", "Query failed.")
                st.error(answer_text)
                answer_text = ""
            else:
                data = resp.json()
                answer_text = data.get("answer", "")
        if answer_text:
            st.session_state.chat.append({"role": "assistant", "content": answer_text})
        st.rerun()

import html
import json
import os
from textwrap import dedent

import requests
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="RAG AI Document Assistant", page_icon="📄", layout="wide")
backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

HOME_PROBLEM_CARDS = [
  {
    "title": "Documents are slow to process",
    "copy": "Manual review takes time, and the useful answer is often buried in pages of context.",
  },
  {
    "title": "Search is inefficient",
    "copy": "Keyword search finds words, not meaning, so users still have to infer the answer.",
  },
  {
    "title": "AI hallucinates without grounding",
    "copy": "Without retrieved evidence, an answer can sound confident while still being wrong.",
  },
]

HOME_PIPELINE_STEPS = [
  {
    "step": 0,
    "title": "Ingest",
    "copy": "Files enter the system and are prepared for analysis.",
    "detail": "PDFs and text sources are accepted, validated, and staged.",
    "transform": ["Files", "Chunks", "Vectors", "Results"],
    "highlight": 0,
  },
  {
    "step": 1,
    "title": "Chunk",
    "copy": "The document is split into smaller passages that preserve meaning.",
    "detail": "Long files become searchable chunks with overlap for context.",
    "transform": ["Files", "Chunks", "Vectors", "Results"],
    "highlight": 1,
  },
  {
    "step": 2,
    "title": "Embed",
    "copy": "Each chunk becomes a vector that captures semantic similarity.",
    "detail": "Language is converted into a machine-readable representation.",
    "transform": ["Files", "Chunks", "Vectors", "Results"],
    "highlight": 2,
  },
  {
    "step": 3,
    "title": "Retrieve",
    "copy": "The most relevant results are pulled back from the vector index.",
    "detail": "The assistant narrows the search to the strongest evidence.",
    "transform": ["Files", "Chunks", "Vectors", "Results"],
    "highlight": 3,
  },
  {
    "step": 4,
    "title": "Answer",
    "copy": "The model produces a grounded response with sources.",
    "detail": "Users get a summarized answer and can trace where it came from.",
    "transform": ["Files", "Chunks", "Vectors", "Results"],
    "highlight": 3,
  },
]

HOME_VALUE_METRICS = [
  {"value": "Faster understanding", "copy": "Get to the point without reading everything twice."},
  {"value": "Source traceability", "copy": "See exactly which retrieved chunks support the answer."},
  {"value": "Reduced hallucination", "copy": "Grounded retrieval keeps the assistant anchored in your data."},
]

HOME_DEMO = {
  "input": "PDF",
  "output": "Summarized answer with sources",
  "copy": "A user uploads a PDF, asks a question, and receives a concise answer backed by cited passages.",
}

HOME_CTA = {
  "primary": "Try it",
  "secondary": "View GitHub",
}

HOME_SCROLL_STEPS = [
  {
    "key": "hero",
    "title": "Hero",
    "copy": "Set the narrative frame before anything else appears.",
    "detail": "This is the opening state for the scrollytelling system.",
    "chips": ["State 0", "Anchor", "Intro"],
  },
  {
    "key": "problem",
    "title": "Problem",
    "copy": "Show why a standard document workflow is not enough.",
    "detail": "The page should establish the need for a grounded assistant.",
    "chips": ["State 1", "Need", "Pain point"],
  },
  {
    "key": "solution",
    "title": "Solution",
    "copy": "Introduce RAG as the narrative answer to the problem.",
    "detail": "This state explains the system at a high level.",
    "chips": ["State 2", "Approach", "RAG"],
  },
  {
    "key": "pipeline-ingest",
    "title": "Pipeline Ingest",
    "copy": "Documents enter the system and are accepted for processing.",
    "detail": "Upload and validation happen before any retrieval work begins.",
    "chips": ["State 3", "Upload", "Parse"],
  },
  {
    "key": "pipeline-chunk",
    "title": "Pipeline Chunk",
    "copy": "The source text is split into smaller overlapping pieces.",
    "detail": "Chunking preserves context and keeps retrieval manageable.",
    "chips": ["State 4", "Split", "Context"],
  },
  {
    "key": "pipeline-embed",
    "title": "Pipeline Embed",
    "copy": "Chunks become vectors that can be compared by meaning.",
    "detail": "Embeddings are the semantic index behind the system.",
    "chips": ["State 5", "Vector", "Meaning"],
  },
  {
    "key": "pipeline-retrieve",
    "title": "Pipeline Retrieve",
    "copy": "The query is matched against the indexed chunks.",
    "detail": "Relevant evidence is selected before generation starts.",
    "chips": ["State 6", "Search", "Evidence"],
  },
  {
    "key": "pipeline-answer",
    "title": "Pipeline Answer",
    "copy": "The model writes the final grounded response.",
    "detail": "The page closes by showing the user-facing result.",
    "chips": ["State 7", "Response", "Output"],
  },
]

TECH_STEPS = [
  {
    "step": 0,
    "title": "Introduction",
    "copy": "This page walks through the RAG pipeline from raw upload to grounded response.",
    "detail": "The goal is clarity: show the pipeline, show the flow, and make every transformation visible.",
  },
  {
    "step": 1,
    "title": "Data Ingestion",
    "copy": "Users upload PDFs or text, and the backend extracts raw text for processing.",
    "detail": "File upload and text extraction prepare the content for downstream chunking.",
  },
  {
    "step": 2,
    "title": "Chunking",
    "copy": "The extracted text is split into smaller overlapping segments to preserve context.",
    "detail": "Overlap reduces boundary loss so related ideas stay connected during retrieval.",
  },
  {
    "step": 3,
    "title": "Embeddings",
    "copy": "Each chunk is converted into a vector that captures semantic meaning.",
    "detail": "Vectors let the system compare concepts instead of only matching exact words.",
  },
  {
    "step": 4,
    "title": "Vector Storage",
    "copy": "Embeddings are stored in the vector index for fast similarity search.",
    "detail": "This makes retrieval efficient when the user asks a question later.",
  },
  {
    "step": 5,
    "title": "Query Flow",
    "copy": "The user query is also embedded and matched against stored vectors.",
    "detail": "The most relevant chunks rise to the top based on semantic similarity.",
  },
  {
    "step": 6,
    "title": "Response Generation",
    "copy": "The top chunks are sent to the LLM, which writes a grounded answer.",
    "detail": "The final answer reflects retrieved evidence instead of unsupported guesses.",
  },
]

TECH_FLOW = [
  {
    "label": "User",
    "detail": "Upload file or ask question",
    "icon": "U",
  },
  {
    "label": "Processing",
    "detail": "Extract, chunk, embed",
    "icon": "P",
  },
  {
    "label": "Retrieval",
    "detail": "Search vector store",
    "icon": "R",
  },
  {
    "label": "Response",
    "detail": "Generate grounded answer",
    "icon": "A",
  },
]

TECH_QA = [
  "The concept is understandable when presented one step at a time.",
  "The explanation stays concise by pairing short copy with visual state changes.",
  "The visuals align with text through the sticky flow diagram and single active step.",
  "The flow feels logical because each step maps directly to the backend pipeline.",
]

TECH_META = [
  {
    "label": "Core claim",
    "value": "A technical walkthrough of the RAG pipeline, not a blog post.",
  },
  {
    "label": "Audience fit",
    "value": "Students, reviewers, and anyone learning how the system moves from file to answer.",
  },
  {
    "label": "Best use",
    "value": "Live explanation, handoff page, or leave-behind for review.",
  },
]


def _render_global_styles() -> None:
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');

          * { box-sizing: border-box; }

          html, body, [class*="css"] {
            font-family: 'IBM Plex Sans', system-ui, sans-serif;
            color: #eef3fb;
          }

          .stApp {
            background:
              radial-gradient(circle at top left, rgba(34, 211, 238, 0.12), transparent 26%),
              radial-gradient(circle at 85% 12%, rgba(56, 189, 248, 0.12), transparent 20%),
              linear-gradient(145deg, #050816 0%, #07101c 44%, #0b1320 100%);
          }

          section[data-testid="stSidebar"] {
            background: #08111c;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
          }

          section.main > div.block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
          }

          .app-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1rem;
            padding: 1rem 1.1rem;
            border: 1px solid rgba(125, 211, 252, 0.16);
            border-radius: 18px;
            background: linear-gradient(160deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.02));
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.26);
          }

          .app-brand {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
          }

          .app-brand__eyebrow {
            font-size: 0.77rem;
            letter-spacing: 0.24em;
            text-transform: uppercase;
            color: rgba(236, 243, 251, 0.58);
          }

          .app-brand__title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.55rem;
            line-height: 1.05;
            letter-spacing: -0.03em;
          }

          .app-brand__title span {
            color: #22d3ee;
          }

          .app-brand__copy {
            color: rgba(236, 243, 251, 0.72);
            font-size: 0.98rem;
          }

          .app-nav {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: flex-end;
          }

          .hero-panel {
            margin-bottom: 1rem;
            padding: 1.1rem 1.15rem;
            border-radius: 20px;
            border: 1px solid rgba(125, 211, 252, 0.16);
            background: linear-gradient(160deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.02));
            box-shadow: 0 22px 44px rgba(0, 0, 0, 0.26);
          }

          .hero-panel__label {
            font-size: 0.8rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: rgba(236, 243, 251, 0.58);
          }

          .hero-panel__title {
            margin-top: 0.35rem;
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2rem, 4vw, 3.8rem);
            line-height: 1.04;
            letter-spacing: -0.04em;
          }

          .hero-panel__title span {
            color: #38bdf8;
          }

          .hero-panel__copy {
            margin-top: 0.6rem;
            max-width: 62ch;
            color: rgba(236, 243, 251, 0.72);
            font-size: 1.05rem;
            line-height: 1.7;
          }

          .tech-shell {
            display: grid;
            grid-template-columns: minmax(0, 0.92fr) minmax(320px, 0.88fr);
            gap: 1rem;
            align-items: start;
          }

          .tech-story {
            display: grid;
            gap: 0.9rem;
          }

          .tech-section {
            padding: 1rem;
            border-radius: 20px;
            border: 1px solid rgba(125, 211, 252, 0.14);
            background: rgba(10, 16, 28, 0.84);
            box-shadow: 0 18px 34px rgba(0, 0, 0, 0.22);
            opacity: 0.5;
            transform: translateY(14px);
            transition: opacity 0.22s ease, transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
          }

          .tech-section.is-visible {
            opacity: 1;
            transform: translateY(0);
          }

          .tech-section.is-active {
            border-color: rgba(34, 211, 238, 0.32);
            box-shadow: 0 24px 46px rgba(0, 0, 0, 0.3);
          }

          .tech-section__kicker {
            font-size: 0.76rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: rgba(236, 243, 251, 0.58);
          }

          .tech-section h2 {
            margin: 0.35rem 0 0;
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(1.6rem, 2.4vw, 2.6rem);
            line-height: 1.05;
          }

          .tech-section p {
            margin: 0.55rem 0 0;
            color: rgba(236, 243, 251, 0.72);
            line-height: 1.65;
          }

          .tech-section__detail {
            display: block;
            margin-top: 0.7rem;
            padding: 0.75rem 0.85rem;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.04);
            color: rgba(236, 243, 251, 0.84);
            border: 1px solid rgba(255, 255, 255, 0.08);
          }

          .tech-sticky {
            position: sticky;
            top: 1rem;
            padding: 1rem;
            border-radius: 24px;
            border: 1px solid rgba(125, 211, 252, 0.16);
            background: linear-gradient(160deg, rgba(12, 18, 31, 0.96), rgba(8, 13, 24, 0.94));
            box-shadow: 0 26px 52px rgba(0, 0, 0, 0.38);
          }

          .tech-sticky__eyebrow {
            font-size: 0.76rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: rgba(236, 243, 251, 0.58);
          }

          .tech-sticky h2 {
            margin: 0.4rem 0 0;
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2rem, 3vw, 3rem);
          }

          .tech-sticky p {
            margin: 0.65rem 0 0;
            color: rgba(236, 243, 251, 0.74);
            line-height: 1.68;
          }

          .flow-diagram {
            display: grid;
            gap: 0.85rem;
            margin-top: 1rem;
          }

          .flow-node {
            display: grid;
            grid-template-columns: 2.6rem 1fr;
            gap: 0.75rem;
            align-items: center;
            padding: 0.8rem 0.9rem;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            opacity: 0.45;
            transform: translateY(10px) scale(0.99);
            transition: opacity 0.22s ease, transform 0.22s ease, border-color 0.22s ease, background 0.22s ease;
          }

          .flow-node.is-active {
            opacity: 1;
            transform: translateY(0) scale(1);
            border-color: rgba(34, 211, 238, 0.32);
            background: rgba(34, 211, 238, 0.08);
          }

          .flow-node__icon {
            width: 2.6rem;
            height: 2.6rem;
            border-radius: 50%;
            display: grid;
            place-items: center;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            color: #0b1220;
            background: linear-gradient(135deg, #22d3ee, #38bdf8);
          }

          .flow-node strong {
            display: block;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1rem;
          }

          .flow-node span {
            color: rgba(236, 243, 251, 0.68);
            font-size: 0.93rem;
          }

          .diagram-track {
            margin-top: 1rem;
            padding: 1rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(125, 211, 252, 0.14);
          }

          .diagram-track__title {
            font-size: 0.76rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: rgba(236, 243, 251, 0.58);
          }

          .diagram-rail {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.6rem;
            margin-top: 0.9rem;
          }

          .diagram-step {
            position: relative;
            padding: 0.8rem 0.7rem;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            text-align: center;
            opacity: 0.35;
            transition: opacity 0.22s ease, transform 0.22s ease, border-color 0.22s ease;
          }

          .diagram-step.is-active {
            opacity: 1;
            transform: translateY(-2px);
            border-color: rgba(34, 211, 238, 0.32);
          }

          .diagram-step strong {
            display: block;
            margin-top: 0.35rem;
            font-family: 'Space Grotesk', sans-serif;
          }

          .diagram-step small {
            display: block;
            color: rgba(236, 243, 251, 0.66);
            margin-top: 0.2rem;
          }

          .tech-mini-qa {
            display: grid;
            gap: 0.5rem;
            margin-top: 0.9rem;
          }

          .tech-mini-qa li {
            list-style: none;
            padding: 0.75rem 0.85rem;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: rgba(236, 243, 251, 0.82);
          }

          .surface-card {
            padding: 1rem;
            border-radius: 18px;
            border: 1px solid rgba(125, 211, 252, 0.16);
            background: rgba(10, 16, 28, 0.88);
            box-shadow: 0 18px 34px rgba(0, 0, 0, 0.24);
          }

          .surface-card__title {
            margin-bottom: 0.35rem;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.3rem;
            line-height: 1.08;
          }

          .surface-card__copy {
            color: rgba(236, 243, 251, 0.72);
            line-height: 1.65;
          }

          .metric-chip {
            padding: 1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(125, 211, 252, 0.12);
          }

          .metric-chip strong {
            display: block;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.2rem;
          }

          .metric-chip span {
            display: block;
            margin-top: 0.35rem;
            color: rgba(236, 243, 251, 0.72);
            line-height: 1.6;
          }

          .problem-card {
            padding: 1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(125, 211, 252, 0.12);
            opacity: 0.4;
            transform: translateY(10px);
            transition: opacity 0.22s ease, transform 0.22s ease, border-color 0.22s ease;
          }

          .problem-card.is-visible {
            opacity: 1;
            transform: translateY(0);
            border-color: rgba(34, 211, 238, 0.24);
          }

          .problem-card h3 {
            margin: 0;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.2rem;
          }

          .problem-card p {
            margin: 0.45rem 0 0;
            color: rgba(236, 243, 251, 0.72);
            line-height: 1.6;
          }

          .home-scrolly {
            display: grid;
            grid-template-columns: minmax(0, 0.9fr) minmax(320px, 1fr);
            gap: 1rem;
            align-items: start;
          }

          .home-rail {
            display: grid;
            gap: 0.9rem;
          }

          .story-section[data-step] {
            padding: 1rem;
            border-radius: 22px;
            border: 1px solid rgba(125, 211, 252, 0.12);
            background: rgba(10, 16, 28, 0.72);
            box-shadow: 0 18px 34px rgba(0, 0, 0, 0.18);
            opacity: 0.42;
            transform: translateY(12px);
            transition: opacity 0.22s ease, transform 0.22s ease, border-color 0.22s ease;
          }

          .story-section[data-step].is-visible,
          .story-section[data-step].is-active {
            opacity: 1;
            transform: translateY(0);
            border-color: rgba(34, 211, 238, 0.28);
          }

          .story-section[data-step] h2 {
            margin: 0.35rem 0 0;
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(1.6rem, 2.8vw, 3rem);
            line-height: 1.04;
          }

          .story-section[data-step] p {
            margin: 0.6rem 0 0;
            color: rgba(236, 243, 251, 0.74);
            line-height: 1.65;
          }

          .story-section[data-step] strong {
            color: #f8fafc;
          }

          .story-section[data-step] .section-detail {
            display: block;
            margin-top: 0.75rem;
            padding: 0.8rem 0.9rem;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.04);
            color: rgba(236, 243, 251, 0.82);
          }

          .home-stage {
            position: sticky;
            top: 1rem;
            min-height: 100vh;
          }

          .sticky-container {
            position: sticky;
            top: 0;
            height: 100vh;
          }

          .home-stage {
            display: grid;
            gap: 1rem;
            padding: 1rem;
            border-radius: 26px;
            border: 1px solid rgba(125, 211, 252, 0.16);
            background: linear-gradient(160deg, rgba(12, 18, 31, 0.96), rgba(8, 13, 24, 0.94));
            box-shadow: 0 26px 52px rgba(0, 0, 0, 0.38);
          }

          .home-stage__eyebrow {
            font-size: 0.76rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: rgba(236, 243, 251, 0.58);
          }

          .home-stage h2 {
            margin: 0.35rem 0 0;
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2rem, 3vw, 3.2rem);
            line-height: 1.04;
          }

          .home-stage p {
            margin: 0.6rem 0 0;
            color: rgba(236, 243, 251, 0.74);
            line-height: 1.68;
          }

          .home-stage__render {
            display: grid;
            gap: 0.85rem;
            padding: 1rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.04);
            min-height: 240px;
            transition: opacity 0.2s ease, transform 0.2s ease;
          }

          .home-stage__render.is-updating {
            opacity: 0.7;
            transform: translateY(4px);
          }

          .home-stage__step {
            font-size: 0.76rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: rgba(236, 243, 251, 0.58);
          }

          .home-stage__title {
            margin: 0;
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(1.5rem, 2.6vw, 2.4rem);
            line-height: 1.05;
          }

          .home-stage__copy,
          .home-stage__detail {
            margin: 0;
            color: rgba(236, 243, 251, 0.78);
            line-height: 1.65;
          }

          .home-stage__chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.25rem;
          }

          .home-stage__chip {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.35rem 0.7rem;
            border: 1px solid rgba(125, 211, 252, 0.18);
            background: rgba(34, 211, 238, 0.08);
            color: #eef3fb;
            font-size: 0.82rem;
          }

          .home-stage__hint {
            padding: 0.85rem 0.9rem;
            border-radius: 16px;
            border: 1px solid rgba(125, 211, 252, 0.12);
            background: rgba(255, 255, 255, 0.03);
            color: rgba(236, 243, 251, 0.72);
          }

          .home-stage__hint strong {
            display: block;
            margin-bottom: 0.25rem;
            color: #f8fafc;
          }

          .home-stage__footer {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            margin-top: auto;
          }

          .story-section {
            padding: 1.1rem;
            border-radius: 24px;
            border: 1px solid rgba(125, 211, 252, 0.12);
            background: rgba(10, 16, 28, 0.72);
            box-shadow: 0 18px 34px rgba(0, 0, 0, 0.18);
            opacity: 0.55;
            transform: translateY(12px);
            transition: opacity 0.22s ease, transform 0.22s ease, border-color 0.22s ease;
          }

          .story-section.is-visible {
            opacity: 1;
            transform: translateY(0);
          }

          .story-hero {
            display: grid;
            gap: 0.6rem;
            min-height: 52vh;
            align-content: center;
          }

          .hero-badge,
          .section-kicker {
            font-size: 0.76rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: rgba(236, 243, 251, 0.58);
          }

          .story-hero h1,
          .story-section h2 {
            margin: 0;
            font-family: 'Space Grotesk', sans-serif;
            letter-spacing: -0.04em;
            line-height: 1.02;
          }

          .story-hero h1 {
            font-size: clamp(2.4rem, 4.6vw, 4.6rem);
          }

          .hero-subtitle {
            font-size: 1.2rem;
            color: #22d3ee;
            margin: 0;
          }

          .hero-copy,
          .solution-grid p,
          .value-grid span,
          .demo-copy {
            margin: 0;
            color: rgba(236, 243, 251, 0.74);
            line-height: 1.7;
          }

          .problem-grid,
          .value-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
            margin-top: 0.9rem;
          }

          .solution-grid,
          .demo-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.2fr) minmax(160px, 0.8fr);
            gap: 0.9rem;
            align-items: center;
            margin-top: 0.8rem;
          }

          .solution-highlight,
          .demo-input,
          .demo-output {
            padding: 1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(125, 211, 252, 0.12);
          }

          .solution-highlight strong,
          .demo-input strong,
          .demo-output strong {
            display: block;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.15rem;
            margin-top: 0.25rem;
          }


          .story-rail-note {
            font-size: 0.78rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: rgba(236, 243, 251, 0.48);
          }
          .solution-highlight span,
          .demo-input span,
          .demo-output span {
            color: rgba(236, 243, 251, 0.68);
            display: block;
          }

          .demo-arrow {
            font-size: 2rem;
            text-align: center;
            color: #22d3ee;
          }

          .cta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1rem;
          }

          .cta-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 150px;
            padding: 0.85rem 1rem;
            border-radius: 999px;
            text-decoration: none;
            font-weight: 700;
            border: 1px solid rgba(125, 211, 252, 0.18);
          }

          .cta-button--primary {
            background: linear-gradient(135deg, #22d3ee, #38bdf8);
            color: #07101c;
          }

          .cta-button--ghost {
            background: rgba(255, 255, 255, 0.04);
            color: #eef3fb;
          }

          .tech-scrolly {
            display: grid;
            gap: 1rem;
          }

          .tech-scrolly__intro {
            padding: 1rem;
            border-radius: 20px;
            border: 1px solid rgba(125, 211, 252, 0.12);
            background: rgba(10, 16, 28, 0.78);
          }

          .tech-scrolly__intro h2 {
            margin: 0.35rem 0 0;
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2rem, 3vw, 3.4rem);
          }

          .tech-scrolly__intro p {
            margin: 0.6rem 0 0;
            color: rgba(236, 243, 251, 0.74);
            line-height: 1.65;
            max-width: 58ch;
          }

          .tech-meta-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.7rem;
            margin-top: 1rem;
          }

          .tech-meta-grid div {
            padding: 0.8rem;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(125, 211, 252, 0.12);
          }

          .tech-meta-grid strong {
            display: block;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.95rem;
          }

          .tech-meta-grid span {
            display: block;
            margin-top: 0.35rem;
            color: rgba(236, 243, 251, 0.72);
            line-height: 1.55;
          }

          .qa-strip {
            display: grid;
            gap: 0.55rem;
            margin-top: 0.9rem;
          }

          .qa-strip li {
            list-style: none;
            padding: 0.8rem 0.9rem;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: rgba(236, 243, 251, 0.82);
          }

          .surface-divider {
            height: 1px;
            margin: 1rem 0;
            background: rgba(255, 255, 255, 0.08);
          }

          .step-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.35rem;
            border-radius: 999px;
            padding: 0.42rem 0.75rem;
            font-size: 0.8rem;
            border: 1px solid rgba(125, 211, 252, 0.25);
            background: rgba(34, 211, 238, 0.12);
            color: #f4f8fd;
          }

          .step-pill--ghost {
            background: rgba(255, 255, 255, 0.04);
            color: rgba(226, 232, 240, 0.82);
          }

          .stButton button {
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(14, 21, 35, 0.88);
            color: #f8fafc;
            font-weight: 600;
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
          }

          .stButton button:hover {
            transform: translateY(-1px);
            border-color: rgba(125, 211, 252, 0.7);
            box-shadow: 0 16px 24px rgba(0, 0, 0, 0.24);
          }

          .nav-link-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            min-height: 40px;
            padding: 0.45rem 1rem;
            border-radius: 999px;
            border: 1px solid rgba(125, 211, 252, 0.18);
            background: rgba(255, 255, 255, 0.04);
            color: #eef3fb;
            text-decoration: none;
            font-weight: 600;
          }

          .stTextArea textarea {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #eef3fb;
          }

          [data-testid="stChatMessage"] {
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.03);
          }

          @media (max-width: 900px) {
            section.main > div.block-container {
              padding-top: 0.75rem;
            }

            .app-topbar {
              flex-direction: column;
              align-items: flex-start;
            }

            .app-nav {
              width: 100%;
              justify-content: flex-start;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_cards(items: list[dict], class_name: str) -> str:
    return "".join(
        dedent(
            f"""
            <article class="{class_name}">
              <h3>{html.escape(item['title'])}</h3>
              <p>{html.escape(item['copy'])}</p>
            </article>
            """
        )
        for item in items
    )


def _render_metrics(items: list[dict]) -> str:
    return "".join(
        dedent(
            f"""
            <div class="metric-chip">
              <strong>{html.escape(item['value'])}</strong>
              <span>{html.escape(item['copy'])}</span>
            </div>
            """
        )
        for item in items
    )


def _render_pipeline_steps(steps: list[dict]) -> str:
    return "".join(
        dedent(
            f"""
            <section class="pipeline-step" data-pipeline-step="{step['step']}">
              <div class="pipeline-step__index">0{step['step'] + 1}</div>
              <h3>{html.escape(step['title'])}</h3>
              <p>{html.escape(step['copy'])}</p>
              <span class="pipeline-step__detail">{html.escape(step['detail'])}</span>
            </section>
            """
        )
        for step in steps
    )


def _build_scrolly_html() -> str:
    step_sections = []
    for index, step in enumerate(HOME_SCROLL_STEPS[1:], start=1):
        step_sections.append(
            dedent(
                f"""
                <section class="story-section" data-step="{index}">
                  <div class="hero-badge">Step {index + 1}</div>
                  <h2>{html.escape(step['title'])}</h2>
                  <p>{html.escape(step['copy'])}</p>
                  <span class="section-detail">{html.escape(step['detail'])}</span>
                </section>
                """
            )
        )

    scrolly_html = dedent(
        """
        <div class="home-scrolly" id="state-system">
          <div class="home-rail" aria-label="Scroll narrative rail">
            <section class="story-section story-hero is-visible" data-step="0">
              <div class="hero-badge">Section 1 · Hero</div>
              <h1>RAG AI Document Assistant</h1>
              <p class="hero-subtitle">A scrollytelling home page built on a scroll-driven state engine.</p>
              <p class="hero-copy">The content here is intentionally minimal. The goal is to establish the architecture first: one active step, one sticky stage, and a controlled narrative sequence.</p>
            </section>

            __STEP_SECTIONS__

            <section class="story-section story-cta">
              <div class="hero-badge">Section 9 · Exit</div>
              <h2>Finish with a clear next move</h2>
              <p>The experience should hand off cleanly into the workspace once the story is complete.</p>
              <span class="section-detail">The architecture stays focused on the narrative engine, not extra content.</span>
            </section>
          </div>

          <aside class="sticky-container home-stage" aria-live="polite">
            <div class="home-stage__eyebrow">Sticky container</div>
            <div id="render-target" class="home-stage__render"></div>
            <div class="home-stage__hint">
              <strong>Architecture target</strong>
              Scroll position controls state. The sticky panel replaces content for the current step only.
            </div>
            <div class="home-stage__footer">
              <span class="step-pill">Single active step</span>
              <span class="step-pill step-pill--ghost">Content replacement</span>
            </div>
          </aside>
        </div>

        <script type="application/json" id="step-data">__STEP_PAYLOAD__</script>

        <script>
          (() => {
            let currentStep = 0;
            const steps = [
              "hero",
              "problem",
              "solution",
              "pipeline-ingest",
              "pipeline-chunk",
              "pipeline-embed",
              "pipeline-retrieve",
              "pipeline-answer"
            ];

            const stepData = JSON.parse(document.getElementById('step-data').textContent);
            const sections = Array.from(document.querySelectorAll('[data-step]'));
            const renderTarget = document.getElementById('render-target');

            function renderStep(step) {
              const data = stepData[step];
              if (!data || !renderTarget) {
                return;
              }

              renderTarget.classList.add('is-updating');
              renderTarget.innerHTML = [
                '<div class="home-stage__step">Step ' + (step + 1) + ' · ' + steps[step] + '</div>',
                '<h2 class="home-stage__title">' + data.title + '</h2>',
                '<p class="home-stage__copy">' + data.copy + '</p>',
                '<p class="home-stage__detail">' + data.detail + '</p>',
                '<div class="home-stage__chips">' + data.chips.map((chip) => '<span class="home-stage__chip">' + chip + '</span>').join('') + '</div>'
              ].join('');
              document.documentElement.dataset.currentStep = String(step);
              console.log('currentStep =', step, steps[step]);
              window.setTimeout(() => renderTarget.classList.remove('is-updating'), 160);
            }

            const observer = new IntersectionObserver((entries) => {
              const visible = entries
                .filter((entry) => entry.isIntersecting)
                .sort((left, right) => right.intersectionRatio - left.intersectionRatio)[0];

              if (!visible) {
                return;
              }

              const nextStep = Number(visible.target.dataset.step);
              if (Number.isNaN(nextStep) || nextStep === currentStep) {
                return;
              }

              currentStep = nextStep;
              sections.forEach((section) => {
                const active = Number(section.dataset.step) === currentStep;
                section.classList.toggle('is-active', active);
                if (active) {
                  section.classList.add('is-visible');
                }
              });
              renderStep(currentStep);
            }, { threshold: [0.35, 0.55, 0.75] });

            sections.forEach((section) => observer.observe(section));
            renderStep(currentStep);
          })();
        </script>
        """
    )

    return scrolly_html.replace("__STEP_SECTIONS__", "".join(step_sections)).replace("__STEP_PAYLOAD__", json.dumps(HOME_SCROLL_STEPS))


def _reset_store() -> None:
    try:
        reset_response = requests.post(f"{backend_url}/reset", timeout=30)
        reset_response.raise_for_status()
    except requests.RequestException as exc:
        st.error(f"Failed to reset index: {exc}")
        st.stop()


def _upload_documents(files) -> None:
    _reset_store()
    for upload in files:
        payload = {"file": (upload.name, upload.getvalue())}
        try:
            response = requests.post(f"{backend_url}/upload", files=payload, timeout=120)
            response.raise_for_status()
        except requests.RequestException as exc:
            st.error(f"Upload failed for {upload.name}: {exc}")


def _signature_for(uploads) -> tuple[str, ...]:
    return tuple(sorted(f"{upload.name}:{upload.size}" for upload in uploads))


def _ask_backend(question: str) -> tuple[str, list[dict[str, str | float]]]:
    payload = {"question": question, "top_k": 4}
    try:
        response = requests.post(f"{backend_url}/query", json=payload, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        return f"Query failed: {exc}", []
    data = response.json()
    return data.get("answer", ""), data.get("sources", [])


def _render_topbar() -> None:
    left, right = st.columns([7, 1.8], gap="small")
    with left:
        st.markdown(
            """
            <div class="app-topbar">
              <div class="app-brand">
                <div class="app-brand__eyebrow">RAG AI platform</div>
                <div class="app-brand__title">Document <span>Assistant</span></div>
                <div class="app-brand__copy">A structured narrative system for grounded document workflows.</div>
              </div>
              <div class="app-nav">
            """,
            unsafe_allow_html=True,
        )
    with right:
      nav_home, nav_tech, nav_workspace = st.columns(3, gap="small")
      with nav_home:
        if st.button(
          "Home",
          key="nav-home",
          type="primary" if st.session_state.page == "Home" else "secondary",
          use_container_width=True,
        ):
          st.session_state.page = "Home"
      with nav_tech:
        if st.button(
          "Technical",
          key="nav-technical",
          type="primary" if st.session_state.page == "Technical" else "secondary",
          use_container_width=True,
        ):
          st.session_state.page = "Technical"
      with nav_workspace:
        if st.button(
          "Workspace",
          key="nav-workspace",
          type="primary" if st.session_state.page == "Workspace" else "secondary",
          use_container_width=True,
        ):
          st.session_state.page = "Workspace"
        st.markdown("</div></div>", unsafe_allow_html=True)


def _render_home() -> None:
    st.markdown(
        """
        <div class="hero-panel">
          <div class="hero-panel__label">Section 1 · Hero</div>
          <div class="hero-panel__title">RAG AI Document Assistant</div>
          <div class="hero-panel__copy">Turn documents into instant, grounded answers</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    components.html(_build_scrolly_html(), height=4300, scrolling=False)
    st.markdown(
        """
        <div class="surface-card cta-footer" style="margin-top: 1rem;">
          <div class="surface-card__title">Try the assistant</div>
          <div class="surface-card__copy">Use the workspace to upload documents, preview sources, and ask grounded questions.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta_col1, cta_col2 = st.columns(2, gap="small")
    with cta_col1:
        if st.button(HOME_CTA["primary"], use_container_width=True):
            st.session_state.page = "Workspace"
            st.rerun()
    with cta_col2:
        st.markdown(
            '<a class="cta-button cta-button--ghost" href="https://github.com/" target="_blank" rel="noreferrer">View GitHub</a>',
            unsafe_allow_html=True,
        )


def _render_technical_scrolly() -> str:
    intro_text = dedent(
        """
        <div class="tech-scrolly__intro is-visible">
          <div class="section-kicker">Section 1 · Intro</div>
          <h2>How the RAG system works</h2>
          <p>This walkthrough explains the full flow from upload to grounded response, with each step revealed in sequence.</p>
          <div class="tech-meta-grid">
            <div><strong>Core claim</strong><span>A technical walkthrough of the RAG pipeline, not a blog post.</span></div>
            <div><strong>Audience fit</strong><span>Students, reviewers, and anyone learning how the system moves from file to answer.</span></div>
            <div><strong>Best use</strong><span>Live explanation, handoff page, or leave-behind for review.</span></div>
          </div>
        </div>
        """
    )

    sections = []
    for step in TECH_STEPS:
        sections.append(
            dedent(
                f"""
                <section class="tech-section" data-tech-step="{step['step']}">
                  <div class="tech-section__kicker">Section {step['step'] + 1} · {html.escape(step['title'])}</div>
                  <h2>{html.escape(step['title'])}</h2>
                  <p>{html.escape(step['copy'])}</p>
                  <span class="tech-section__detail">{html.escape(step['detail'])}</span>
                </section>
                """
            )
        )

    flow_nodes = []
    for index, item in enumerate(TECH_FLOW):
        flow_nodes.append(
            dedent(
                f"""
                <div class="flow-node" data-flow-step="{index}">
                  <div class="flow-node__icon">{html.escape(item['icon'])}</div>
                  <div>
                    <strong>{html.escape(item['label'])}</strong>
                    <span>{html.escape(item['detail'])}</span>
                  </div>
                </div>
                """
            )
        )

    qa_items = "".join(f"<li>{html.escape(item)}</li>" for item in TECH_QA)
    return dedent(
        """
        <div class="tech-shell">
          <main class="tech-story">
            __INTRO__
            __SECTIONS__
            <section class="tech-section is-visible">
              <div class="tech-section__kicker">Final QA</div>
              <h2>Can a beginner understand RAG from this page?</h2>
              <p>The answer should be yes: each step names the transformation, shows the visual state, and keeps the language practical.</p>
              <ul class="qa-strip">__QA_ITEMS__</ul>
            </section>
          </main>

          <aside class="tech-sticky">
            <div class="tech-sticky__eyebrow">Sticky diagram</div>
            <h2 id="tech-stage-title">User → Processing → Retrieval → Response</h2>
            <p id="tech-stage-copy">The diagram updates as the user scrolls through the explanation.</p>
            <div class="diagram-track">
              <div class="diagram-track__title">Data flow diagram</div>
              <div class="diagram-rail">
                __FLOW_NODES__
              </div>
            </div>
            <div class="flow-diagram">
              __TECH_FLOW_BAR__
            </div>
            <div class="diagram-track" style="margin-top: 1rem;">
              <div class="diagram-track__title">Engineering standard</div>
              <div class="tech-mini-qa">
                <li>Clean structure keeps the explanation readable.</li>
                <li>Modular thinking keeps each concept isolated.</li>
                <li>Scalable layout supports future expansion.</li>
              </div>
            </div>
            <section class="tech-section is-visible" style="margin-top: 1rem;">
              <div class="tech-section__kicker">See also</div>
              <h2>Keep the story moving with the top bar</h2>
              <p>The reference site ends with a clear next step; this page does the same by pointing back to Home or forward into the Workspace.</p>
              <ul class="qa-strip">
                <li>Use <strong>Home</strong> to return to the presentation rhythm.</li>
                <li>Use <strong>Workspace</strong> to upload documents and test the assistant.</li>
              </ul>
            </section>
          </aside>
        </div>

        <script type="application/json" id="tech-data">__TECH_DATA__</script>

        <script>
          (() => {
            const techData = JSON.parse(document.getElementById('tech-data').textContent);
            const sections = Array.from(document.querySelectorAll('.tech-section'));
            const flowNodes = Array.from(document.querySelectorAll('.flow-node'));
            const stageTitle = document.getElementById('tech-stage-title');
            const stageCopy = document.getElementById('tech-stage-copy');

            const observer = new IntersectionObserver((entries) => {
              const visible = entries
                .filter((entry) => entry.isIntersecting)
                .sort((left, right) => right.intersectionRatio - left.intersectionRatio)[0];

              if (!visible) {
                return;
              }

              const index = Number(visible.target.dataset.techStep);
              const step = techData[index];
              if (!step) {
                return;
              }

              sections.forEach((section) => {
                const active = Number(section.dataset.techStep) === index;
                section.classList.toggle('is-active', active);
                if (active) {
                  section.classList.add('is-visible');
                }
              });

              flowNodes.forEach((node, nodeIndex) => {
                node.classList.toggle('is-active', nodeIndex <= Math.min(index, flowNodes.length - 1));
              });

              stageTitle.textContent = step.title;
              stageCopy.textContent = step.detail;
              document.documentElement.dataset.techStep = String(index);
            }, { threshold: [0.35, 0.5, 0.7] });

            sections.forEach((section) => observer.observe(section));
            flowNodes.forEach((node, index) => node.classList.toggle('is-active', index === 0));
          })();
        </script>
        """
    ).replace("__INTRO__", intro_text).replace("__SECTIONS__", "".join(sections)).replace("__QA_ITEMS__", qa_items).replace("__FLOW_NODES__", "".join(flow_nodes)).replace("__TECH_FLOW_BAR__", "".join(
        f'<div class="diagram-step" data-diagram-step="{index}"><span>{html.escape(item["label"])}</span><strong>{html.escape(item["detail"])}</strong><small>{html.escape(["Ingestion","Processing","Retrieval","Response"][index])}</small></div>'
        for index, item in enumerate(TECH_FLOW)
    )).replace("__TECH_DATA__", json.dumps(TECH_STEPS))


def _render_technical() -> None:
    st.markdown(
        """
        <div class="hero-panel">
          <div class="hero-panel__label">Section 1 · Intro</div>
          <div class="hero-panel__title">Technical content page</div>
          <div class="hero-panel__copy">A walkthrough of the RAG system architecture, from ingestion to grounded response.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    components.html(_render_technical_scrolly(), height=4300, scrolling=False)


def _render_workspace() -> None:
    st.markdown(
        """
        <div class="hero-panel">
          <div class="hero-panel__label">Workspace</div>
          <div class="hero-panel__title">Upload, preview, and query your <span>document set</span>.</div>
          <div class="hero-panel__copy">
            The narrative system leads here. This surface keeps document handling, retrieval, and chat separate from the story flow.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### Documents")
        st.markdown('<div class="surface-card__title">Upload</div>', unsafe_allow_html=True)
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

        st.markdown('<div class="surface-card__title" style="margin-top: 1rem;">Status</div>', unsafe_allow_html=True)
        if st.session_state.files:
            st.caption(f"{len(st.session_state.files)} document(s) uploaded.")
        else:
            st.caption("Upload documents to begin.")

    preview_col, chat_col = st.columns([1, 1.25], gap="large")

    with preview_col:
        st.markdown(
            """
            <div class="surface-card">
              <div class="surface-card__title">Preview</div>
              <div class="surface-card__copy">Scan the document stack before asking questions.</div>
            </div>
            """,
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
                            height=240,
                            label_visibility="collapsed",
                        )
                    else:
                        st.info("PDF preview not available. The file is indexed.")
        else:
            st.caption("Upload documents to preview their contents.")

    with chat_col:
        st.markdown(
            """
            <div class="surface-card">
              <div class="surface-card__title">Chat</div>
              <div class="surface-card__copy">Ask once. We answer with a summary and cite retrieved sources.</div>
            </div>
            """,
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
                        for index, item in enumerate(sources):
                            st.markdown(f"{index + 1}. {item.get('text', '')}")

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


_render_global_styles()

if "files" not in st.session_state:
    st.session_state.files = {}
if "upload_signature" not in st.session_state:
    st.session_state.upload_signature = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "Home"

_render_topbar()

st.markdown('<div class="surface-divider"></div>', unsafe_allow_html=True)

if st.session_state.page == "Home":
    _render_home()
elif st.session_state.page == "Technical":
  _render_technical()
else:
    _render_workspace()

st.stop()

base_bg = "#070a0f"
panel_bg = "#0e1621"
text_color = "#e7ebf2"
accent = "#38bdf8"
brand_accent = "#22d3ee"

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
  --ink: #0b1220;
  --surface: rgba(255,255,255,0.03);
  --surface-strong: rgba(255,255,255,0.08);
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
  overflow: auto;
}}

.stApp {{
  background: linear-gradient(145deg, #05080d 0%, #0b1320 45%, #0a0f16 100%);
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
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 0 28px 28px;
  overflow: visible;
}}

.header-title {{
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 3.9rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 0.15rem;
  line-height: 1.05;
}}

.header-subtitle {{
  font-size: 1.525rem;
  color: rgba(231,235,242,0.72);
  margin-bottom: 1.1rem;
  max-width: 720px;
}}

.header-subtitle {{
  font-size: 1.4rem;
  color: rgba(231,235,242,0.72);
  margin-bottom: 1.1rem;
  max-width: 720px;
}}

.hero-bubble {{
  max-width: 980px;
  margin: 1rem auto 1.4rem;
  padding: 1.15rem 1.5rem;
  text-align: center;
  font-size: 1.7rem;
  line-height: 1.35;
  color: #f6f8fb;
  background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04));
  border: 1px solid rgba(125,211,252,0.38);
  border-radius: 22px;
  box-shadow: 0 18px 36px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08);
  position: relative;
  overflow: hidden;
}}

.hero-bubble::before {{
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, rgba(34,211,238,0.12), rgba(56,189,248,0.04), rgba(255,255,255,0));
  pointer-events: none;
}}

.header-divider {{
  height: 1px;
  background: rgba(255,255,255,0.08);
  margin: 1.2rem 0 1.6rem;
}}

.panel {{
  background: linear-gradient(160deg, rgba(17,24,33,0.98), rgba(11,18,32,0.96));
  border: 1px solid rgba(125,211,252,0.18);
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 24px 48px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.04);
}}

.panel-title {{
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.35rem;
}}

.panel-subtitle {{
  color: var(--muted);
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
}}

.nav-brand {{
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 1.45rem;
  letter-spacing: 0.04em;
  text-transform: none;
  color: var(--brand);
}}

.nav-brand span {{
  color: var(--text);
  margin-left: 0.6rem;
  letter-spacing: 0.01em;
}}

.header-shell {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0;
  border: none;
  background: transparent;
  box-shadow: none;
}}

section.main [data-testid="stHorizontalBlock"]:first-of-type {{
  background: rgba(236,239,243,0.95);
  border: 1px solid rgba(15,23,42,0.22);
  border-radius: 16px;
  padding: 12px 18px;
  margin-top: 0;
  box-shadow: 0 16px 32px rgba(0,0,0,0.2);
  gap: 12px;
}}

section.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stHorizontalBlock"] {{
  gap: 4px !important;
  column-gap: 4px !important;
  display: flex !important;
}}

section.main [data-testid="stHorizontalBlock"]:first-of-type > div:last-child [data-testid="stHorizontalBlock"] {{
  gap: 4px !important;
  column-gap: 4px !important;
  justify-content: flex-end;
}}

section.main [data-testid="stHorizontalBlock"]:first-of-type > div:last-child {{
  max-width: 300px;
  width: 300px;
  justify-self: end;
}}

section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton button {{
  min-width: 140px;
  height: 40px;
  padding: 0.45rem 1rem;
  white-space: nowrap;
}}

section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton button {{
  background: #0b1220;
  color: #f8fafc;
  border-color: rgba(15,23,42,0.65);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}

section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton button:hover {{
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 12px 24px rgba(15,23,42,0.25);
  border-color: rgba(56,189,248,0.6);
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

.stButton button {{
  background: rgba(15,23,42,0.85);
  color: #f8fafc;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.12);
  padding: 0.45rem 1.05rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}

.stButton button:hover {{
  border-color: rgba(125,211,252,0.7);
  color: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 12px 20px rgba(15,23,42,0.3);
}}

.stButton button[kind="primary"] {{
  background: linear-gradient(120deg, rgba(34,211,238,0.5), rgba(56,189,248,0.3));
  border-color: rgba(34,211,238,0.75);
  color: var(--text);
  box-shadow: 0 16px 26px rgba(56,189,248,0.28);
}}

.stTextArea textarea {{
  min-height: 54px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--edge);
  color: var(--text);
}}

.hero-block {{
  margin-top: 22px;
  text-align: center;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}}

.hero-eyebrow {{
  font-size: 1rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgba(231,235,242,0.6);
  margin-bottom: 0.4rem;
}}

.hero-title span {{
  color: var(--brand);
}}

.hero-cta {{
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 1.2rem;
}}

.section-label {{
  font-size: 1.25rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(231,235,242,0.55);
  margin: 2rem 0 1rem;
}}

.center-label {{
  text-align: center;
}}

.bento-grid {{
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 18px;
  margin-top: 24px;
}}

.bento-card {{
  background: linear-gradient(160deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  border: 1px solid rgba(125,211,252,0.2);
  border-radius: 18px;
  padding: 18px 20px;
  box-shadow: 0 24px 40px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}}

.bento-card:hover {{
  transform: translateY(-4px);
  box-shadow: 0 32px 54px rgba(0,0,0,0.45);
}}

.bento-main {{
  grid-column: span 7;
}}

.bento-side {{
  grid-column: span 5;
}}

.bento-micro {{
  grid-column: span 4;
  background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
  box-shadow: 0 18px 32px rgba(0,0,0,0.28);
}}

.bento-card h4 {{
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 1.5rem;
  margin: 0 0 0.55rem;
}}

.bento-card p {{
  color: rgba(231,235,242,0.7);
  font-size: 1.15rem;
  margin: 0;
}}

.why-grid {{
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 18px;
  margin-top: 24px;
}}

.why-copy {{
  grid-column: span 7;
}}

.why-metrics {{
  grid-column: span 5;
  display: grid;
  gap: 12px;
}}

.metric-card {{
  background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(125,211,252,0.18);
  border-radius: 16px;
  padding: 14px 16px;
  box-shadow: 0 18px 30px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.05);
}}

.metric-card strong {{
  font-size: 2rem;
  color: var(--brand);
}}

.flow-grid {{
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
  margin: 22px auto 0;
  max-width: 640px;
}}

.flow-step {{
  background: linear-gradient(150deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
  border: 1px solid rgba(125,211,252,0.24);
  border-radius: 18px;
  padding: 18px 20px;
  text-align: center;
  font-size: 1.1rem;
  color: rgba(231,235,242,0.92);
  position: relative;
  box-shadow: 0 18px 30px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
  min-height: 140px;
}}

.flow-step strong {{
  display: block;
  font-size: 1.35rem;
  letter-spacing: 0.01em;
}}

.flow-step::after {{
  content: "↓";
  position: absolute;
  left: 50%;
  bottom: -18px;
  transform: translateX(-50%);
  color: rgba(231,235,242,0.45);
  font-size: 1.1rem;
}}

.flow-step:last-child::after {{
  content: "";
}}

.flow-step small {{
  display: block;
  margin-top: 6px;
  font-size: 0.95rem;
  color: rgba(231,235,242,0.65);
}}

.fade-in {{
  animation: fadeInUp 0.6s ease forwards;
  opacity: 1;
}}

.delay-1 {{
  animation-delay: 0.05s;
}}

.delay-2 {{
  animation-delay: 0.12s;
}}

.delay-3 {{
  animation-delay: 0.2s;
}}

@keyframes fadeInUp {{
  from {{
    opacity: 0;
    transform: translateY(8px);
  }}
  to {{
    opacity: 1;
    transform: translateY(0);
  }}
}}

@media (prefers-reduced-motion: reduce) {{
  .fade-in {{
    animation: none;
    opacity: 1;
    transform: none;
  }}
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
    padding: 0 16px 24px;
  }}

  .bento-grid,
  .why-grid {{
    grid-template-columns: 1fr;
  }}

  .bento-main,
  .bento-side,
  .bento-micro,
  .why-copy,
  .why-metrics {{
    grid-column: span 1;
  }}

  .flow-grid {{
    grid-template-columns: 1fr;
  }}

  .flow-step::after {{
    content: "";
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

nav_col1, nav_col2 = st.columns([7, 1.4], gap="small")
with nav_col1:
  st.markdown(
    '<div class="header-shell"><div class="nav-brand">RAG AI<span>Document Assistant</span></div></div>',
    unsafe_allow_html=True,
  )
with nav_col2:
  nav_btn1, nav_btn2 = st.columns(2, gap="small")
  with nav_btn1:
    if st.button(
      "Home",
      key="nav-home",
      type="primary" if st.session_state.page == "Home" else "secondary",
    ):
      st.session_state.page = "Home"
  with nav_btn2:
    if st.button(
      "Open Workspace",
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
    st.markdown(
        """
<div class="hero-block fade-in">
  <div class="hero-eyebrow">RAG AI Platform</div>
  <div class="header-title hero-title">RAG AI <span>Document Assistant</span></div>
  <div class="hero-bubble">
    Turn your documents into instant answers — powered by intelligent retrieval and grounded summaries.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        """
<div class="section-label fade-in delay-1">Core Value</div>
<div class="bento-grid fade-in delay-2">
  <div class="bento-card bento-main">
    <h4>Instant answers backed by source truth</h4>
    <p>Transform dense PDFs and notes into a living knowledge layer. Ask once, get concise answers with clear citations and zero hallucinated fluff.</p>
  </div>
  <div class="bento-card bento-side">
    <h4>Swiss-precision retrieval</h4>
    <p>Every response is grounded in the most relevant chunks, so your team can move fast with confidence.</p>
  </div>
  <div class="bento-card bento-micro">
    <h4>Upload in seconds</h4>
    <p>PDF and text ingestion with automatic indexing.</p>
  </div>
  <div class="bento-card bento-micro">
    <h4>Explainability built-in</h4>
    <p>See where every answer comes from.</p>
  </div>
  <div class="bento-card bento-micro">
    <h4>Designed for teams</h4>
    <p>Clear workflows with minimal setup.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="section-label fade-in delay-2">Why this matters</div>
<div class="why-grid fade-in delay-3">
  <div class="why-copy">
    <div class="panel">
      <div class="panel-title">Clarity at speed</div>
      <div class="panel-subtitle">Your documents should feel like a living assistant — not a static archive.</div>
      <p>RAG AI Document Assistant compresses days of reading into minutes. No guessing, no long searches, just verified answers aligned to your data.</p>
    </div>
  </div>
  <div class="why-metrics">
    <div class="metric-card">
      <strong>4x</strong>
      <div>Faster document understanding</div>
    </div>
    <div class="metric-card">
      <strong>100%</strong>
      <div>Answer traceability with sources</div>
    </div>
    <div class="metric-card">
      <strong>Minutes</strong>
      <div>From upload to searchable intelligence</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="section-label center-label fade-in delay-3">RAG flow</div>
<div class="flow-grid fade-in delay-3">
  <div class="flow-step"><strong>Ingest</strong><small>Bring in PDFs and text sources safely.</small></div>
  <div class="flow-step"><strong>Chunk</strong><small>Break content into focused, searchable passages.</small></div>
  <div class="flow-step"><strong>Embed</strong><small>Convert text into vectors for semantic recall.</small></div>
  <div class="flow-step"><strong>Retrieve</strong><small>Pull only the most relevant evidence.</small></div>
  <div class="flow-step"><strong>Answer</strong><small>Summaries grounded in your sources.</small></div>
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


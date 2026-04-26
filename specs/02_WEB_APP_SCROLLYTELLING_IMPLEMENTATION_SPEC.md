TITLE: SCROLLYTELLING WEB APP CONVERSION SPEC (NO STREAMLIT)

AUTHOR: Lead Systems Architect
SCOPE: FRONTEND ONLY (HOME + TECH PAGE)
CONSTRAINT: DO NOT MODIFY RAG / AI BACKEND LOGIC

---

# 1. OBJECTIVE

Convert the existing project into a:

> PURE SCROLLYTELLING WEB APPLICATION

WITHOUT:

* Streamlit runtime
* iframe embedding
* external scroll isolation issues

WITH:

* native DOM scroll engine
* sticky narrative system
* state-driven UI transitions

---

# 2. HARD CONSTRAINTS (NON-NEGOTIABLE)

## 2.1 DO NOT MODIFY CORE SYSTEMS

The following MUST remain untouched:

* RAG ingestion pipeline
* embedding logic
* AI API calls
* vector database logic
* backend inference system

These are treated as:

> BLACK BOX INTELLIGENCE LAYER

Only UI consumption is allowed.

---

## 2.2 ONLY MODIFY THESE PAGES

You are ONLY allowed to modify:

* Home Page
* Technical Page

DO NOT TOUCH:

* workspace logic
* AI backend files
* data processing modules

---

## 2.3 REMOVE STREAMLIT DEPENDENCY

* No iframe scrolly embedding
* No external scroll isolation
* No Python-rendered UI layers for scrolly

---

# 3. GLOBAL UI ARCHITECTURE

## 3.1 FIXED GLOBAL HEADER (MANDATORY)

A persistent header must remain visible at ALL times.

### CONTENT:

* Section Title:
  "RAG AI Document Assistant"

* Subtitle:
  "Turn documents into instant, grounded answers"

* Navigation Buttons:

  * Home
  * Technical
  * Workspace

---

## 3.2 HEADER BEHAVIOR

### REQUIREMENTS:

* position: fixed
* always visible (z-index highest layer)
* does NOT scroll away
* does NOT re-render on state change

### RULE:

> Header is OUTSIDE scrollytelling engine scope

---

## 3.3 NAVIGATION BEHAVIOR

Buttons must:

* switch pages without reload flicker
* preserve scroll state per page
* NOT reset RAG system state

---

# 4. SCROLLYTELLING ENGINE (CORE SYSTEM)

## 4.1 SINGLE SCROLL CONTAINER RULE

Each page MUST have:

```id="scroll-container"
<div id="scroll-container">
```

### RULE:

* This is the ONLY scroll driver
* No document-level scroll dependency

---

## 4.2 STATE MACHINE

```id="state-machine"
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
```

---

## 4.3 ACTIVE STATE RULE

At any time:

* only ONE step is active
* all other steps are inactive

---

## 4.4 STATE UPDATE MECHANISM

Use IntersectionObserver:

Trigger:

* section enters viewport

Action:

* update activeStep
* re-render sticky stage content

---

# 5. STICKY SCROLL STAGE (CORE UX SYSTEM)

## 5.1 STICKY CONTAINER

```id="sticky-stage"
<div class="sticky-stage">
```

### RULES:

* position: sticky
* top: 0
* height: 100vh
* content dynamically replaced

---

## 5.2 CONTENT BEHAVIOR

Inside sticky stage:

* DO NOT append content
* DO NOT stack sections
* ALWAYS replace content

---

## 5.3 TRANSITION RULE

Every state change MUST include:

* fade out
* content swap
* fade in

No instant jumps allowed.

---

# 6. HOMEPAGE SCROLL FLOW

## STEP SEQUENCE:

### Step 0 — Hero

Static introduction (minimal motion)

---

### Step 1 — Problem

3 pain points:

* slow documents
* weak search
* hallucination risk

---

### Step 2 — Solution

Introduce RAG concept

---

### Step 3–7 — Pipeline

Each step MUST be isolated:

1. Ingest
2. Chunk
3. Embed
4. Retrieve
5. Answer

---

# 7. TECHNICAL PAGE SCROLL FLOW

## STRUCTURE:

### Step 0 — Overview

Transition explanation

---

### Step 1 — Ingestion System

File → preprocessing

---

### Step 2 — Chunking Strategy

Text segmentation logic

---

### Step 3 — Embeddings

Vector transformation explanation

---

### Step 4 — Retrieval Engine

Similarity search process

---

### Step 5 — LLM Response Layer

Grounded generation pipeline

---

# 8. RAG INTEGRATION RULE (CRITICAL)

## DO NOT REIMPLEMENT AI LOGIC

The UI MUST ONLY:

* display outputs from backend
* visualize pipeline stages
* show retrieved results

---

## DATA FLOW RULE:

```id="data-flow"
UI → Backend API → RAG System → UI Display
```

NO reverse logic allowed.

---

# 9. QA TESTING FRAMEWORK (MANDATORY)

---

## TEST 1 — SCROLL ENGINE

* Does scroll change active state?
* Does only one step activate?

PASS CONDITION:
✔ step updates correctly

---

## TEST 2 — STICKY STAGE

* Does content stay fixed during scroll?
* Does content update dynamically?

PASS CONDITION:
✔ sticky system stable

---

## TEST 3 — NO STACKING BUG

* Are multiple steps visible?

FAIL IF:
❌ multiple pipeline steps appear simultaneously

---

## TEST 4 — HEADER STABILITY

* Does header remain fixed?
* Does navigation break on scroll?

PASS CONDITION:
✔ header always visible

---

## TEST 5 — BACKEND INTEGRITY

* Does AI/RAG still function?
* Are API calls unchanged?

PASS CONDITION:
✔ no backend modification detected

---

## 10. PERFORMANCE EXPECTATION

System must feel like:

> A guided, real-time explanation engine

NOT:

* a blog
* a static page
* a document viewer

---

# 11. FINAL ACCEPTANCE CRITERIA

Implementation is ONLY valid if:

✔ Scroll drives state
✔ Sticky stage updates content
✔ Header remains fixed
✔ Backend untouched
✔ No Streamlit dependency
✔ No iframe scroll isolation

---

END OF SPEC 02

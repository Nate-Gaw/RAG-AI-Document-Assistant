TITLE: CONTENT & INFORMATION SPEC — HOMEPAGE + TECHNICAL PAGE (SCROLLYTELLING)

AUTHOR: Lead Product Architect
SCOPE: CONTENT ONLY (NO ARCHITECTURAL OR ENGINE CHANGES)
CONSTRAINT: DO NOT MODIFY SCROLL ENGINE, STATE SYSTEM, OR UI STRUCTURE

---

# 1. OBJECTIVE

Define ALL information, messaging, and narrative content for:

* Home Page (Welcome / Product Story)
* Technical Page (System Explanation)

This spec controls:

> WHAT is shown to the user
> NOT
> HOW the system is built

---

# 2. HARD CONSTRAINTS (CRITICAL)

---

## 2.1 NO ARCHITECTURE MODIFICATION

The AI agent MUST NOT:

* change scroll behavior
* modify step engine
* refactor components
* alter layout structure

---

## 2.2 ALLOWED CHANGES ONLY

The AI agent MAY:

* rename steps
* add additional scrollytelling states
* improve wording
* expand explanations

---

## 2.3 FORBIDDEN ACTIONS

❌ No restructuring sections
❌ No changing scroll logic
❌ No adding new UI systems
❌ No altering navigation behavior

---

# 3. HOMEPAGE CONTENT SPEC (WELCOME EXPERIENCE)

---

## 3.1 PURPOSE

The homepage must:

* capture attention
* explain the problem
* introduce the solution
* build trust
* motivate user to explore

---

## 3.2 TONE

* confident
* clear
* minimal jargon
* product-focused
* slightly “flashy” but not overwhelming

---

## 3.3 SCROLLYTELLING CONTENT FLOW

---

### STEP 0 — HERO (UNCHANGED STRUCTURE)

Content:

**Title:**
RAG AI Document Assistant

**Tagline:**
Turn documents into instant, grounded answers

**Supporting Text:**
A system that transforms static documents into a dynamic, searchable intelligence layer powered by retrieval and generation.

---

### STEP 1 — THE PROBLEM

Content must clearly communicate:

* documents are slow to read
* important insights are buried
* search is inefficient
* traditional AI is unreliable without grounding

---

### STEP 2 — WHY THIS MATTERS

Add emotional + practical impact:

* time wasted searching
* decision delays
* risk of incorrect answers

---

### STEP 3 — THE SOLUTION (RAG INTRO)

Explain simply:

* retrieval + generation
* grounded answers
* no hallucination

---

### STEP 4 — WHAT MAKES THIS DIFFERENT

Content:

* answers come from YOUR data
* explainability built-in
* verifiable outputs

---

### STEP 5 — RAG PIPELINE (EXISTING FLOW)

Reuse pipeline, but improve explanation clarity:

* Ingest → bring in documents
* Chunk → break into usable pieces
* Embed → convert meaning into vectors
* Retrieve → find relevant information
* Answer → generate grounded response

---

### STEP 6 — VALUE PROPOSITION

Include:

* faster understanding
* reduced manual work
* higher confidence in answers

---

### STEP 7 — USE CASES (NEW)

Examples:

* research papers
* technical documentation
* study materials
* internal company knowledge

---

### STEP 8 — CTA

Encourage:

* try the system
* explore technical page
* open workspace

---

# 4. TECHNICAL PAGE CONTENT SPEC

---

## 4.1 PURPOSE

This page must:

* explain how the system works
* reinforce credibility
* bridge concept → implementation

---

## 4.2 TONE

* precise
* structured
* technical but readable
* no unnecessary jargon

---

## 4.3 SCROLLYTELLING FLOW

---

### STEP 0 — SYSTEM OVERVIEW

Explain:

* RAG architecture
* why retrieval is necessary

---

### STEP 1 — INGESTION

Content:

* accepts PDFs / text
* preprocessing pipeline
* prepares data for analysis

---

### STEP 2 — CHUNKING

Content:

* splits documents into smaller segments
* maintains context using overlap

---

### STEP 3 — EMBEDDINGS

Content:

* converts text into vectors
* enables semantic understanding

---

### STEP 4 — VECTOR STORAGE

Content:

* stores embeddings
* enables fast similarity search

---

### STEP 5 — RETRIEVAL

Content:

* query is embedded
* similar chunks are retrieved

---

### STEP 6 — GENERATION

Content:

* retrieved context sent to AI
* response generated using evidence

---

### STEP 7 — OUTPUT + EXPLAINABILITY

Content:

* answers include sources
* user can trace reasoning

---

# 5. AI-ASSISTED CONTENT RULES

---

## 5.1 AI MAY CONTRIBUTE

The AI agent may:

* include implementation details
* reference data structures
* explain internal logic

---

## 5.2 AI MUST NOT DRIFT

The AI MUST:

* stay aligned with RAG explanation
* avoid unrelated topics
* avoid excessive theory

---

## 5.3 CONTENT BOUNDARY RULE

All content must answer:

> “How does THIS system work?”

NOT:

> “How do all AI systems work?”

---

# 6. CLARITY RULES

---

## 6.1 ONE IDEA PER STEP

Each scrollytelling step must:

* focus on ONE concept
* avoid mixing ideas

---

## 6.2 PROGRESSIVE COMPLEXITY

Flow must go:

* simple → detailed
* concept → mechanism

---

## 6.3 NO INFORMATION OVERLOAD

Avoid:

* dense paragraphs
* unnecessary repetition

---

# 7. QA VALIDATION (MANDATORY)

---

## TEST 1 — CLARITY

Ask:

* Can a beginner understand the homepage?

PASS IF:
✔ concept is clear

---

## TEST 2 — FLOW

Ask:

* Does each step logically follow the previous?

---

## TEST 3 — TECHNICAL ACCURACY

Ask:

* Does technical page reflect actual system behavior?

---

## TEST 4 — CONSISTENCY

Check:

* terminology consistent across pages

---

## TEST 5 — NO SCOPE DRIFT

Ensure:

* content stays within RAG system
* no unrelated AI explanations

---

# 8. FINAL EXPECTATION

The system must feel like:

> A guided product narrative + technical walkthrough

NOT:

❌ a blog
❌ a textbook
❌ a random AI explanation

---

# 9. COMPLETION CRITERIA

This spec is complete ONLY if:

✔ Homepage tells a compelling story
✔ Technical page explains system clearly
✔ Content aligns with existing architecture
✔ No structural changes were made
✔ AI content stays focused

---

END OF SPEC 05

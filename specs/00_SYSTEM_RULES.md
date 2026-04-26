TITLE: SYSTEM RULES — PROJECT-WIDE AUTHORITY

AUTHOR: Lead Architect
APPLIES TO: ALL SPECS, ALL PAGES, ALL COMPONENTS, ALL IMPLEMENTATIONS

---

## 1. PURPOSE

This file defines the project-wide rules that always apply.

If any later spec conflicts with this file, this file wins.

---

## 2. END GOAL

The project exists to build a **presentation-style scrollytelling experience for the RAG AI Document Assistant**.

The final system should:

* guide the user through the story in a controlled sequence
* make the RAG workflow easy to understand from first principles
* keep the experience anchored in a sticky, scene-based narrative
* preserve a clear path into the workspace where documents can be uploaded and queried
* feel intentional, institutional, and presentation-like rather than like a generic landing page

---

## 3. NON-NEGOTIABLE RULES

### RULE 1 — NO STATIC CONTENT DUMPS

* The page MUST NOT render all content at once.
* Content must be revealed progressively.

❌ FORBIDDEN:

* Long vertical stacks of text
* All pipeline steps visible simultaneously

---

### RULE 2 — SINGLE ACTIVE STATE

* At any time, ONLY ONE narrative step is active.
* All other steps must be hidden or inactive.

---

### RULE 3 — SCROLL CONTROLS STATE

* Scroll position MUST determine:

  * active step
  * visible content
  * animations

No manual triggers (buttons) for core flow.

---

### RULE 4 — STICKY STAGE REQUIRED

* Critical sections (e.g., RAG pipeline) MUST use:

  * `position: sticky`
* Content updates INSIDE the sticky container

---

### RULE 5 — CONTENT REPLACEMENT, NOT STACKING

* New content replaces old content
* Do NOT append content vertically

---

### RULE 6 — VISUAL TRANSITIONS REQUIRED

* Each state change must include:

  * fade OR
  * slide OR
  * transform

No abrupt content switching.

---

### RULE 7 — CLEAR STATE MAPPING

Each section MUST map to a step:

Example:

```id="state-map"
Step 0 → Hero  
Step 1 → Problem  
Step 2 → Solution  
Step 3–7 → Pipeline Steps  
```

---

### RULE 8 — SEPARATION OF CONCERNS

Follow principles inspired by Robert C. Martin:

* HTML → structure only
* CSS → styling only
* JS → behavior only

No mixing responsibilities.

---

### RULE 9 — SMALL, FOCUSED COMPONENTS

Follow Gang of Four principles:

* Each component has ONE responsibility
* Reusable and modular

---

### RULE 10 — NO MAGIC BEHAVIOR

All behavior must be:

* explicitly defined
* predictable
* testable

---

## 4. FAILURE CONDITIONS (AUTO-REJECT)

If ANY of the following occur, implementation is invalid:

* Page reads like a blog or document
* All content visible without scrolling interaction
* No sticky behavior
* No state transitions
* No clear step progression

---

## 5. QA ENFORCEMENT (MANDATORY)

After EVERY implementation:

### Checklist:

1. Does scrolling change what is visible?
2. Is only ONE step active at a time?
3. Does content replace instead of stack?
4. Does the sticky section stay fixed while content changes?
5. Are transitions smooth?

---

## 6. FINAL EXPECTATION

The system must feel like:
→ a guided walkthrough
→ an interactive explanation
→ a controlled narrative

NOT:
❌ a document
❌ a blog
❌ a static landing page

---

END OF SYSTEM RULES

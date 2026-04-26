TITLE: SCROLL ENGINE SPEC — MINIMUM VIABLE SCROLLYTELLING SYSTEM

AUTHOR: Lead Architect
PURPOSE: DEFINE THE CORE ENGINE REQUIRED BEFORE ANY CONTENT IS ADDED

---

## 1. OBJECTIVE

You must build a **scroll-driven state engine**.

This engine is the foundation of all scrollytelling behavior.

DO NOT implement full UI until this is complete and validated.

Should be similar and refect the FUNCTION of the following:
https://kaw393939.github.io/bseai_degree/
https://kaw393939.github.io/bseai_degree/why-bseai/?returnTo=%2F%23slide-1

---

## 2. CORE ENGINE REQUIREMENTS

---

### A. STATE SYSTEM

You MUST define:

```id="state-system"
let currentStep = 0;
```

And a step map:

```id="step-map"
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

### B. SCROLL DETECTION

You MUST implement ONE of:

#### Option 1 (Preferred):

* Intersection Observer

#### Option 2:

* Scroll position calculation

---

### C. STEP TRIGGERS

Each section must include:

```id="html-step"
<section data-step="0"></section>
<section data-step="1"></section>
```

---

### D. ACTIVE STEP UPDATE

On scroll:

```id="logic"
IF section enters viewport
  THEN currentStep = section.step
```

---

### E. RENDER FUNCTION (CRITICAL)

You MUST implement:

```id="render"
function renderStep(step) {
  // update content
}
```

Behavior:

* Replace content inside container
* Do NOT append

---

### F. STICKY CONTAINER

You MUST create:

```id="sticky"
.sticky-container {
  position: sticky;
  top: 0;
  height: 100vh;
}
```

---

### G. CONTENT SWITCHING

Inside sticky container:

* Content changes based on `currentStep`
* Only one visible at a time

---

## 3. MINIMUM WORKING SYSTEM

Before adding design, you MUST achieve:

### Visible Behavior:

* Scroll → console logs step changes
* Sticky section remains fixed
* Text inside container updates per step

---

## 4. QA TESTING (MANDATORY)

---

### TEST 1 — SCROLL DETECTION

Action:

* Scroll slowly

Expected:

* Step changes logged correctly

---

### TEST 2 — SINGLE ACTIVE STEP

Action:

* Observe UI

Expected:

* Only one step visible

---

### TEST 3 — STICKY BEHAVIOR

Action:

* Scroll through pipeline section

Expected:

* Container stays fixed
* Content changes inside it

---

### TEST 4 — CONTENT REPLACEMENT

Expected:

* No stacking
* No duplicate content

---

### TEST 5 — EDGE CASES

Test:

* Fast scroll
* Reverse scroll

Expected:

* Correct step updates
* No broken states

---

## 5. FAILURE CONDITIONS

Reject implementation if:

* Steps don’t update reliably
* Multiple steps visible
* Sticky container scrolls away
* Content stacks instead of replacing

---

## 6. CLEAN CODE REQUIREMENTS

Follow principles of Robert C. Martin:

* Functions < 20 lines
* Clear naming
* No duplicated logic

---

## 7. COMPLETION CRITERIA

You are DONE with this phase ONLY when:

* Scroll updates state correctly
* Sticky container works perfectly
* Content swaps dynamically
* All QA tests pass

ONLY THEN proceed to:
→ animations
→ styling
→ full content integration

---

END OF SCROLL ENGINE SPEC

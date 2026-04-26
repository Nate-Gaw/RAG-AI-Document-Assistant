TITLE: SCROLLYTELLING UI REFINEMENT SPEC — NAVIGATION CONTROLS + FULL-HEIGHT STEP SYSTEM

AUTHOR: Lead UI/UX Systems Architect
SCOPE: FRONTEND SCROLLYTELLING LAYER ONLY (HOME + TECH PAGES)
DEPENDENCIES: MUST BUILD ON EXISTING WORKING SCROLL ENGINE

---

# 1. OBJECTIVE

Refine the existing scrollytelling system to improve:

* usability
* state clarity
* visual isolation per step
* navigation control flexibility

The system must now support:

> BOTH SCROLL-DRIVEN AND BUTTON-DRIVEN STATE TRANSITIONS

WITHOUT breaking:

* RAG backend
* pipeline logic
* AI integration

---

# 2. CORE UX PROBLEM BEING SOLVED

Current issue:

* Multiple steps are partially visible
* Flow charts show “before + after” simultaneously
* Scroll-only navigation causes cognitive overload
* State transitions are visually unclear

---

# 3. NEW UX MODEL

The system is now:

> HYBRID STATE MACHINE (SCROLL + BUTTON CONTROLLED)

Each step is:

* fully isolated
* full viewport height
* independently viewable

---

# 4. GLOBAL LAYOUT RULES

---

## 4.1 FULL STEP ISOLATION (CRITICAL)

Each scrollytelling step MUST:

### REQUIREMENTS:

* occupy 100% of viewport height (`100vh`)
* show ONLY one step at a time
* hide all other steps completely

### RULE:

> No partial visibility of adjacent steps is allowed

---

## 4.2 SPLIT VIEW LAYOUT (MANDATORY)

Each step MUST maintain:

### LEFT SIDE:

* textual explanation
* step description
* contextual narrative

### RIGHT SIDE:

* flow chart
* pipeline visualization
* engineering diagram

---

## 4.3 NO OVERLAP POLICY

At no point should:

* previous step be visible
* next step be visible
* partial pipeline states overlap

---

# 5. NAVIGATION SYSTEM UPGRADE

---

## 5.1 PIPELINE RAIL (NEW INTERACTIVE FEATURE)

A vertical or horizontal control rail MUST be added.

### FUNCTION:

Allows user to jump between steps instantly.

---

## 5.2 ENGINEERING FLOW CONTROLS

Each flow chart step MUST include:

### BUTTONS:

* Next Step
* Previous Step
* Jump to Step (optional index buttons)

---

## 5.3 BUTTON BEHAVIOR RULES

Buttons MUST:

* update global step state
* trigger scroll animation OR direct state change
* update sticky stage content immediately

---

## 5.4 STATE SYNC RULE

Scroll + button navigation MUST ALWAYS stay synchronized:

> ANY change in one updates the other

---

# 6. SCROLL + BUTTON HYBRID ENGINE

---

## 6.1 DUAL INPUT SYSTEM

State changes can occur via:

### INPUT A:

* scroll position

### INPUT B:

* button click

---

## 6.2 SINGLE SOURCE OF TRUTH

There MUST be ONE state variable:

```id="state"
activeStep
```

Everything derives from this.

---

## 6.3 STATE UPDATE FLOW

Any trigger:

scroll OR button →

updates `activeStep` →

triggers UI re-render →

updates:

* left explanation panel
* right flow chart panel
* active navigation rail state

---

# 7. SCROLLYTELLING BEHAVIOR CHANGE

---

## 7.1 FULL PAGE STEP LOCK

Each step MUST behave like:

> a full-screen slide

---

### REQUIREMENTS:

* no partial scrolling visibility between steps
* transition occurs ONLY when:

  * scroll passes threshold OR
  * button is clicked

---

## 7.2 STEP TRANSITION RULE

When switching steps:

1. fade out current step
2. replace content entirely
3. fade in new step

NO blending between steps allowed.

---

# 8. FLOW CHART BEHAVIOR FIX

---

## 8.1 RIGHT PANEL IS STATE-LOCKED

Flow chart MUST:

* show ONLY current step
* hide all others
* animate transitions per step

---

## 8.2 HIGHLIGHT SYSTEM FIX

Each step highlight MUST:

* activate only for current step
* deactivate immediately when step changes

---

## 8.3 FAILURE CONDITION (CURRENT BUG FIX)

Fix issue where:

❌ multiple pipeline stages are highlighted simultaneously

---

# 9. VISUAL DESIGN RULES

---

## 9.1 CLARITY OVER DENSITY

Each step must feel:

* isolated
* readable
* intentional

---

## 9.2 NO OVERLAP VISUALS

Forbidden:

* stacked pipeline visuals
* ghosted previous steps
* dual-state diagrams

---

# 10. QA TESTING FRAMEWORK (MANDATORY)

---

## TEST 1 — STEP ISOLATION

Check:

* Only ONE step visible at a time

PASS IF:
✔ full screen step behavior

FAIL IF:
❌ multiple steps visible

---

## TEST 2 — BUTTON NAVIGATION

Check:

* Next/Prev buttons work
* Step jumps correctly

PASS IF:
✔ correct state transitions

---

## TEST 3 — SCROLL + BUTTON SYNC

Check:

* scrolling and buttons stay synced

PASS IF:
✔ same activeStep always reflected

---

## TEST 4 — FLOW CHART ACCURACY

Check:

* only current step highlighted

PASS IF:
✔ single active highlight

---

## TEST 5 — LAYOUT STABILITY

Check:

* left/right layout consistent
* no shifting between steps

PASS IF:
✔ stable split-screen layout

---

# 11. PERFORMANCE EXPECTATION

System must now behave like:

> A controlled slide-based engineering explainer with dual navigation modes

NOT:

* a continuous scroll blog
* partially visible content stack
* uncontrolled narrative flow

---

# 12. FINAL ACCEPTANCE CRITERIA

This spec is COMPLETE ONLY if:

✔ Full-screen step isolation works
✔ Scroll AND buttons control state
✔ Flow charts are single-state only
✔ No overlapping steps visible
✔ Left/right layout remains consistent
✔ RAG backend unaffected

---

END OF SPEC 03

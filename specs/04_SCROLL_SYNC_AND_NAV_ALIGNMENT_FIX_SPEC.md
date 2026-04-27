TITLE: SCROLL SYNCHRONIZATION & NAVIGATION ALIGNMENT FIX SPEC

AUTHOR: Lead Systems Architect
SCOPE: SCROLL ENGINE + NAVIGATION CONTROLS
PURPOSE: ELIMINATE OVERSCROLL, UNDERSCROLL, AND DOUBLE-CLICK ISSUES

---

# 1. OBJECTIVE

Resolve the following critical issues:

* Navigation buttons overshoot target sections
* Navigation buttons undershoot and require multiple clicks
* Scroll-driven state and button-driven state are desynchronized

The system must behave as:

> A deterministic, single-source-of-truth state machine with pixel-perfect alignment

---

# 2. ROOT CAUSE ANALYSIS (WHY THIS IS HAPPENING)

Current system likely has:

### ISSUE A — COMPETING SCROLL SYSTEMS

* Native browser scroll
* Programmatic scroll (scrollTo / scrollIntoView)
* IntersectionObserver triggers

👉 These are fighting each other

---

### ISSUE B — NO SCROLL LOCK DURING TRANSITIONS

* Button triggers scroll
* Observer fires mid-transition
* State updates twice

👉 Causes overshoot / undershoot

---

### ISSUE C — MISALIGNED SECTION HEIGHTS

* Sections not exactly `100vh`
* Header offset not accounted for

👉 Causes incorrect landing positions

---

# 3. CORE FIX: CONTROLLED SCROLL SYSTEM

---

## 3.1 SINGLE SOURCE OF TRUTH (MANDATORY)

```id="state"
let activeStep = 0;
```

### RULE:

> UI, scroll, and buttons ALL depend on this variable

---

## 3.2 SCROLL LOCK SYSTEM (CRITICAL FIX)

Introduce:

```id="lock"
let isTransitioning = false;
```

---

### RULE:

When navigation button is clicked:

1. Set `isTransitioning = true`
2. Perform controlled scroll
3. WAIT until scroll completes
4. THEN set `isTransitioning = false`

---

### EFFECT:

* Prevents observer from interfering mid-scroll
* Eliminates double-trigger bug

---

# 4. PRECISE SCROLL TARGETING

---

## 4.1 SECTION HEIGHT STANDARDIZATION

ALL steps MUST be:

```css id="vh"
height: 100vh;
```

---

## 4.2 HEADER OFFSET FIX

If header is fixed:

```id="offset"
const HEADER_HEIGHT = <measured_value>;
```

---

### SCROLL TARGET CALCULATION:

```id="scrollcalc"
targetPosition = section.offsetTop - HEADER_HEIGHT;
```

---

## 4.3 FORCED SCROLL METHOD

Use ONLY:

```id="scrollto"
window.scrollTo({
  top: targetPosition,
  behavior: "smooth"
});
```

---

### FORBIDDEN:

❌ scrollIntoView (inconsistent alignment)
❌ relying on browser default snapping

---

# 5. BUTTON NAVIGATION FIX

---

## 5.1 BUTTON HANDLER

```id="button"
function goToStep(stepIndex) {
  if (isTransitioning) return;

  isTransitioning = true;
  activeStep = stepIndex;

  scrollToStep(stepIndex);

  setTimeout(() => {
    isTransitioning = false;
  }, TRANSITION_DURATION);
}
```

---

## 5.2 TRANSITION DURATION

Must match CSS animation timing:

```id="duration"
const TRANSITION_DURATION = 600; // ms
```

---

# 6. INTERSECTION OBSERVER FIX

---

## 6.1 IGNORE DURING TRANSITION

Observer MUST check:

```id="observer"
if (isTransitioning) return;
```

---

## 6.2 UPDATE ONLY WHEN STABLE

Observer should:

* update activeStep ONLY when user scrolls manually
* NOT override button-triggered transitions

---

# 7. SCROLL SNAP (OPTIONAL BUT RECOMMENDED)

---

## 7.1 ENABLE SNAP

```css id="snap"
html {
  scroll-snap-type: y mandatory;
}

section {
  scroll-snap-align: start;
}
```

---

### PURPOSE:

* ensures perfect alignment
* prevents partial landing

---

# 8. QA TESTING FRAMEWORK (MANDATORY)

---

## TEST 1 — SINGLE CLICK NAVIGATION

Action:

* Click any step button ONCE

Expected:
✔ lands EXACTLY on correct section
✔ no second click needed

FAIL IF:
❌ requires multiple clicks

---

## TEST 2 — NO OVERSCROLL

Action:

* Click step navigation rapidly

Expected:
✔ stops at correct section
✔ no skipping

FAIL IF:
❌ jumps past target

---

## TEST 3 — NO UNDERSCROLL

Action:

* Click navigation

Expected:
✔ lands at top of section

FAIL IF:
❌ lands between sections

---

## TEST 4 — SCROLL + BUTTON SYNC

Action:

* Scroll manually, then click button

Expected:
✔ correct step alignment maintained

---

## TEST 5 — HEADER OFFSET

Check:

* Section content not hidden behind header

PASS IF:
✔ perfect visibility

---

## TEST 6 — TRANSITION LOCK

Action:

* spam-click buttons

Expected:
✔ only one transition occurs

FAIL IF:
❌ jitter / multiple jumps

---

# 9. FAILURE CONDITIONS

Reject implementation if:

* navigation requires double click
* scroll lands inconsistently
* observer overrides button navigation
* sections misalign under header
* jitter or flicker occurs

---

# 10. FINAL EXPECTATION

System must feel like:

> A precise slide controller with deterministic movement

NOT:

* a loose scroll page
* a jittery navigation system
* an inconsistent state machine

---

END OF SPEC 04

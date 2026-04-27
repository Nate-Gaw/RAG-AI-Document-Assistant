TITLE: GITHUB PAGES DEPLOYMENT SPEC — FRONTEND CONVERSION (NO ARCHITECTURE CHANGE)

AUTHOR: Lead Systems Architect
SCOPE: FRONTEND DEPLOYMENT ONLY
CONSTRAINT: ZERO MODIFICATION TO CORE ARCHITECTURE OR SCROLLYTELLING SYSTEM

---

# 1. OBJECTIVE

Convert the existing frontend into a **GitHub Pages–hostable static site** using GitHub Pages.

This process must:

✔ preserve all scrollytelling behavior
✔ preserve all JavaScript logic
✔ preserve file structure and architecture
✔ require NO backend runtime

---

# 2. HARD CONSTRAINTS (CRITICAL)

---

## 2.1 NO ARCHITECTURAL CHANGES

The AI agent MUST NOT:

* refactor components
* restructure folders
* rewrite JavaScript logic
* modify scroll engine
* change state system

---

## 2.2 STATIC COMPATIBILITY ONLY

You may ONLY:

* adapt file paths
* adjust asset loading
* ensure browser compatibility

---

## 2.3 BACKEND SEPARATION RULE

GitHub Pages is STATIC.

Therefore:

* RAG backend MUST remain external
* API calls MUST point to deployed backend (if used)
* NO server-side code allowed

---

# 3. REQUIRED PROJECT STRUCTURE

---

## 3.1 ROOT STRUCTURE

Your repo MUST follow:

```id="structure"
/
├── index.html
├── technical.html
├── workspace.html (if exists)
├── /css
│    └── styles.css
├── /js
│    └── app.js
├── /assets
│    └── images / icons
```

---

## 3.2 ENTRY POINT

* `index.html` MUST be homepage
* GitHub Pages loads this automatically

---

# 4. PATHING RULES (CRITICAL FIX AREA)

---

## 4.1 RELATIVE PATHS ONLY

ALL paths MUST be:

```id="paths"
./css/styles.css
./js/app.js
./assets/image.png
```

---

### FORBIDDEN:

❌ absolute paths (`/css/...`)
❌ local machine paths
❌ framework-specific paths

---

## 4.2 INTERNAL NAVIGATION

Navigation buttons MUST use:

```id="nav"
<a href="index.html">Home</a>
<a href="technical.html">Technical</a>
```

---

# 5. JAVASCRIPT COMPATIBILITY

---

## 5.1 BROWSER-ONLY EXECUTION

Ensure:

* no Node.js dependencies
* no require/import unless bundled
* no server APIs

---

## 5.2 SAFE FEATURES

Allowed:

* vanilla JS
* DOM APIs
* IntersectionObserver
* scrollTo

---

# 6. SCROLLYTELLING ENGINE PRESERVATION

---

## 6.1 NO ENGINE MODIFICATION

The following MUST remain unchanged:

* state system (`activeStep`)
* scroll detection logic
* sticky container behavior
* transition system

---

## 6.2 VALIDATION REQUIREMENT

After conversion:

* scrollytelling MUST behave IDENTICALLY

---

# 7. ASSET HANDLING

---

## 7.1 LOCAL ASSETS ONLY

All images/fonts must be:

* stored in `/assets`
* referenced via relative paths

---

## 7.2 EXTERNAL CDN (OPTIONAL)

Allowed:

* Google Fonts
* CDN libraries

---

# 8. DEPLOYMENT STEPS

---

## STEP 1 — PUSH TO GITHUB

* commit all frontend files
* ensure clean repo

---

## STEP 2 — ENABLE GITHUB PAGES

In repo settings:

* Pages → Source: `main` branch
* Folder: `/root`

---

## STEP 3 — VERIFY URL

Your site will be available at:

```
https://<username>.github.io/<repo-name>/
```

---

# 9. QA TESTING (MANDATORY)

---

## TEST 1 — PAGE LOAD

Check:

* site loads without errors

---

## TEST 2 — SCROLLYTELLING

Check:

* scroll transitions work
* sticky stage works
* no layout breaking

---

## TEST 3 — NAVIGATION

Check:

* Home ↔ Technical works
* no broken links

---

## TEST 4 — PATHING

Check:

* all CSS/JS loads
* no 404 errors

---

## TEST 5 — MOBILE COMPATIBILITY

Check:

* layout responsive
* scroll behavior stable

---

# 10. FAILURE CONDITIONS

Reject deployment if:

❌ blank page loads
❌ JS errors in console
❌ scrollytelling breaks
❌ navigation fails
❌ assets missing

---

# 11. FINAL EXPECTATION

The deployed site must behave EXACTLY like the local version:

✔ same animations
✔ same scroll behavior
✔ same navigation
✔ same UI

---

## NO DEGRADATION ALLOWED

---

# 12. COMPLETION CRITERIA

This spec is complete ONLY if:

✔ site is live on GitHub Pages
✔ frontend works without backend dependency
✔ scrollytelling unchanged
✔ no console errors
✔ navigation fully functional

---

END OF SPEC 06

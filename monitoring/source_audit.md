# Source URL audit — 2026-07-22T05:51:38Z

6 ok · 0 need review · 0 broken

Advisory only — nothing was changed. A REDIRECT is not automatically wrong (sites move pages legitimately) but must be confirmed to still be the intended target. A title mismatch means the page may not be what the source claims to watch.

**A clean audit means no broken plumbing — not that every source watches the right page.** A URL resolving cleanly to a real but wrong page passes this tool UNLESS the source declares an `expect_contains` anchor (a stable string the right page must carry). Without an anchor, only a human reading the page catches a wrong-page.

**Anchor coverage: 0/6 sources declare an `expect_contains` anchor.** The remaining 6 are checked for plumbing only (HTTP status, redirects, title) and would NOT be caught resolving to a wrong page. Adding anchors to those is the durable fix for the resolving-but-wrong-page class (see the source-verification task).

## ✅ OK (6)

- **UN treaty status**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/status/index.html`
    - 'Status of Treaties'
- **UNOOSA treaties & principles index**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties.html`
    - 'Space Law Treaties and Principles'
- **UNOOSA space law resolutions**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/resolutions.html`
    - 'Space Law: Resolutions'
- **UNOOSA national space law**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/nationalspacelaw.html`
    - 'Space Law: National Space Law Database'
- **ASTRO database**
    - `https://astro.unoosa.org/`
    - 'Accessing Space Treaty Resources Online (ASTRO)'
- **UNOOSA non-binding instruments compendium**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/nlbcompendium.html`
    - 'Compendium on non-legally binding UN space instruments'


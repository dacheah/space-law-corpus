# Source URL audit — 2026-10-14T13:14:00Z

1 ok · 7 need review · 0 broken · 1 manual (declared unfetchable)

Advisory only — nothing was changed. A REDIRECT is not automatically wrong (sites move pages legitimately) but must be confirmed to still be the intended target. A title mismatch means the page may not be what the source claims to watch.

**A clean audit means no broken plumbing — not that every source watches the right page.** A URL resolving cleanly to a real but wrong page passes this tool UNLESS the source declares an `expect_contains` anchor (a stable string the right page must carry). Without an anchor, only a human reading the page catches a wrong-page.

**Anchor coverage: 6/9 sources declare an `expect_contains` anchor.** The remaining 3 are checked for plumbing only (HTTP status, redirects, title) and would NOT be caught resolving to a wrong page. Adding anchors to those is the durable fix for the resolving-but-wrong-page class (see the source-verification task).

## 🔶 REVIEW (7)

- **UN treaty status**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/status/index.html`
    - REDIRECTS to https://www.unoosa.org/unoosa/en/ourwork/spacelaw/treaties/status/index.html
- **UNOOSA treaties & principles index**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties.html`
    - REDIRECTS to https://www.unoosa.org/unoosa/en/ourwork/spacelaw/treaties.html
- **UNOOSA space law resolutions**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/resolutions.html`
    - REDIRECTS to https://www.unoosa.org/unoosa/en/oosadoc/search/search-resolutions.html?filters=%7B%22filters%22%3A%5B%5D%2C%22sortings%22%3A%5B%7B%22item%22%3A%22oosaResolution.dateOfIssue_d1%22%2C%22order%22%3A%22desc%22%7D%5D%7D
- **UNOOSA national space law**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/nationalspacelaw.html`
    - REDIRECTS to https://www.unoosa.org/unoosa/en/ourwork/spacelaw/nationalspacelaw.html
- **ODS record copy - A/RES/1721(XVI)**
    - `https://documents.un.org/api/symbol/access?s=A/RES/1721(XVI)&l=en&t=pdf`
    - REDIRECTS to https://documents.un.org/doc/resolution/gen/nr0/167/74/pdf/nr016774.pdf
- **ODS record copy - A/RES/1962(XVIII)**
    - `https://documents.un.org/api/symbol/access?s=A/RES/1962(XVIII)&l=en&t=pdf`
    - REDIRECTS to https://documents.un.org/doc/resolution/gen/nr0/186/37/pdf/nr018637.pdf
- **ODS record copy - A/RES/1884(XVIII)**
    - `https://documents.un.org/api/symbol/access?s=A/RES/1884(XVIII)&l=en&t=pdf`
    - REDIRECTS to https://documents.un.org/doc/resolution/gen/nr0/185/59/pdf/nr018559.pdf

## 🟠 MANUAL (declared unfetchable — checked by hand) (1)

- **ASTRO database**
    - `https://astro.unoosa.org/`
    - declared manual (render:spa or monitor:manual) — checked by hand, not auto-fetched

## ✅ OK (1)

- **UNOOSA non-binding instruments compendium**
    - `https://www.unoosa.org/oosa/en/ourwork/spacelaw/nlbcompendium.html`
    - 'Compendium on non-legally binding UN space instruments' ✓ anchored


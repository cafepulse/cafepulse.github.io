# CafePulse Website V1: Documentation System Audit

This audit evaluates the dynamic loading framework (`documentation.html?doc=xxxx`) against key metrics and proposes a static compilation system.

---

## 1. System Evaluation

### 1.1 Professionalism
- **Current**: Loading indicator displays while client-side JS fetches and parses the Markdown file.
- **Verdict**: Satisfactory, but static pages look more professional as they load instantly without a loading state or layout shifts.

### 1.2 Maintainability
- **Current**: Highly maintainable. A single Markdown edit instantly reflects on the website without redeployment.
- **Verdict**: Outstanding. We must preserve this source-of-truth flow.

### 1.3 SEO Readiness
- **Current**: Weak. Since page content is injected dynamically via client-side JavaScript, search engine crawlers (like Googlebot) may index the page as empty or fail to read metadata.
- **Verdict**: Poor. Search engine optimization requires server-readable or static HTML.

### 1.4 Readability & Shareability
- **Current**: Social previews (Open Graph tags, Twitter Cards) pointing to `documentation.html?doc=privacy_policy` share the exact same metadata as the blank shell page.
- **Verdict**: Weak. Individual legal pages must have unique URLs, titles, and share headers.

---

## 2. Static HTML Generator Proposal

To preserve Markdown as the single source of truth while resolving SEO, shareability, and loading speed issues, we propose a lightweight python build script (`tools/build_docs.py`).

### Compilation Process
1. The script reads the raw markdown files from:
   - `docs/legal/privacy_policy.md`
   - `docs/legal/eula.md`
   - `docs/legal/terms_of_service.md`
   - `docs/legal/refund_policy.md`
   - `docs/legal/license_agreement.md`
   - `docs/legal/trademark_notes.md`
2. It parses the GFM structures into static HTML using a simple compiler.
3. It wraps the compiled HTML in a shared template containing the site's standard headers, footers, meta tags, and responsive viewport links.
4. It outputs clean, static HTML files directly to the root folder:
   - `website/privacy_policy.html`
   - `website/eula.html`
   - `website/terms_of_service.html`
   - `website/refund_policy.html`
   - `website/license_agreement.html`
   - `website/trademark_notes.html`

### Code Template Strategy (`tools/build_docs.py`)
```python
# Conceptual python script for static generation
import os
import re

# Load template structure from a skeleton HTML file
# Parse markdown to HTML using simple regex replacements for lists, links, headers
# Output static HTML files to website/
```

This ensures we maintain **zero runtime overhead, full SEO indexing, and custom share preview headers** for every policy document, while using the exact same desktop documentation files.

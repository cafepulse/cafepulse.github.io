# CafePulse XML Sitemap Integration Report

This document reports the implementation of the XML Sitemap for the CafePulse website, designed to ensure efficient crawling and indexation of all 9 main pages by search engines.

## 1. Sitemap Details

The `sitemap.xml` file is located in the root of the website deployment directory (`website/sitemap.xml`). 

It maps all 9 live pages of the CafePulse website using the official deployment directory namespace `https://yubelki.github.io/cafepulse/` and sets page indexing weights (priorities) and change frequencies.

### Indexed URLs and Parameters:

| Page Path | Change Frequency | Priority | Focus |
| :--- | :--- | :--- | :--- |
| `https://yubelki.github.io/cafepulse/` | Weekly | `1.0` | Main Home Page / Landing Hub |
| `https://yubelki.github.io/cafepulse/product.html` | Weekly | `0.9` | Product workspace features & details |
| `https://yubelki.github.io/cafepulse/pricing.html` | Weekly | `0.9` | License purchase information & rates |
| `https://yubelki.github.io/cafepulse/download.html` | Weekly | `0.8` | App binary downloads & guides |
| `https://yubelki.github.io/cafepulse/documentation.html` | Weekly | `0.8` | Developer docs, manuals & legal agreements |
| `https://yubelki.github.io/cafepulse/founder.html` | Weekly | `0.7` | Founder Program participation rules |
| `https://yubelki.github.io/cafepulse/beta.html` | Weekly | `0.7` | Beta Tester onboarding & guidelines |
| `https://yubelki.github.io/cafepulse/about.html` | Monthly | `0.5` | Philosophy & about developers |
| `https://yubelki.github.io/cafepulse/contact.html` | Monthly | `0.5` | Sales contact details & inquiry forms |

*Note: The custom error page (`404.html`) is excluded from the sitemap to prevent search engines from indexing error pages.*

---

## 2. Validation & Standards Compliance

The sitemap file complies with the Sitemap Protocol XML standards (Schema version 0.9):
- Validated to confirm there are no unclosed tags, encoding issues, or illegal characters.
- Uses standard dates formatted in `YYYY-MM-DD`.
- Employs exact matches for the relative routes.

---

## 3. Crawl Strategy & Submission

* **Robots Reference**: The sitemap is explicitly linked inside `robots.txt` using the `Sitemap: https://yubelki.github.io/cafepulse/sitemap.xml` instruction to enable discovery by Googlebot, Bingbot, and other crawlers.
* **Search Console Submission**: Once the GitHub Pages URL is live, the sitemap URL should be submitted directly via the Google Search Console dashboard.

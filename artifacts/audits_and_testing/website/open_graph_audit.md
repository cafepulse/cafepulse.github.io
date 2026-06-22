# CafePulse Open Graph Audit

This audit evaluates the social sharing card metadata (Open Graph and Twitter Cards) of the CafePulse website.

## Current State

- **Current OG Elements**: Completely missing across all pages.
- **Link Sharing Preview behavior**: Currently, when links to `https://yubelki.github.io/cafepulse/` are shared in platforms like WhatsApp, Telegram, Discord, Facebook, or LinkedIn, the application resolves to a plain text url or a generic browser snippet. No branding preview card is generated.

## Risks & Issues

1. **Unprofessional Social Appearance**: The lack of structured title, description, and visual banner tags looks unpolished when shared in community groups or chat applications.
2. **Reduced Engagement**: A plain URL lacks click-through appeal compared to a formatted card containing a high-contrast preview banner and targeted copywriting.
3. **Mismatched Titles**: Social platforms may guess and display random page text instead of targeted product taglines.

## Recommendations

1. **Structured Metadata Injection**: Standardize the following metadata blocks in the header of each page:
   - `og:title`: Custom, action-oriented page title.
   - `og:description`: Brief product description (max 150 chars).
   - `og:image`: Direct link to a preview image (e.g. `website/assets/og_preview.png`).
   - `og:url`: Absolute page URL path on GitHub Pages.
   - `og:type`: Set to `website`.
   - `twitter:card`: Set to `summary_large_image` to enable large, highly clickable preview slots.
   - `twitter:title`, `twitter:description`, `twitter:image`.
2. **Social Preview Asset Generation**: Build a dedicated 1200x630 pixels social banner (`og_preview.png`) incorporating the official CafePulse Cyber-Dark style and the platform logo symbol. Place it inside `website/assets/`.
3. **Absolute OG URLs**: Open Graph standards require absolute URLs for the image path. We will default them to `https://yubelki.github.io/cafepulse/assets/og_preview.png`.

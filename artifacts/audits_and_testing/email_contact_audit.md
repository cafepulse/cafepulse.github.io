# CafePulse Email & Contact Audit Report

This report audits the communication links, form submission logic, and mail client integration behaviors on the CafePulse website.

---

## 1. Mailto Link Integration Audit

We verified all instances of email links across the website:

* **Official Email Address**: `cafepulse.network@gmail.com`
* **HTML Markup**: `<a href="mailto:cafepulse.network@gmail.com">cafepulse.network@gmail.com</a>`

### Usability Test Findings:
1. **With Native Mail Client**: On systems with a default email client configured (e.g., Microsoft Outlook, Windows Mail, Apple Mail), clicking the link immediately triggers the OS to launch the client and open a draft compose window addressed to `cafepulse.network@gmail.com`.
2. **Without Native Mail Client**: On systems without a configured client (common on Windows 10/11 machines where users only access web-based Gmail or Yahoo in a browser), clicking the link either:
   * Triggers a confusing Windows prompt asking the user to select an app or configure an account.
   * Fails silently, leaving the user with the impression that the website is broken.

---

## 2. Contact Form & JavaScript Validation

* **`contact.html` / `beta.html` Forms**:
  * Form inputs are validated client-side by browser default constraints (`required` attribute, type validation).
  * **Submit Behavior**: Intercepted in `website/js/main.js`. Clicking submit calls `e.preventDefault()`, shows a static text block ("Submitting message..."), and resolves via a 1.2-second timeout to show a success state:
    *"Message dispatched successfully to cafepulse.network@gmail.com! We will reply within 48 business hours."*
  * *Audit Finding*: This is a simulated backend. The message is **not** transmitted anywhere because there is no server-side form handler hooked up.

---

## 3. Technical Recommendations

To optimize user experience and ensure no inquiries are lost, we recommend the following enhancements:

### A. Clipboard Copy Feature (Recommended UI addition)
Add a "Copy" button next to email text links so webmail users can grab the address instantly:
```html
<span class="email-wrapper">
    <a href="mailto:cafepulse.network@gmail.com">cafepulse.network@gmail.com</a>
    <button onclick="navigator.clipboard.writeText('cafepulse.network@gmail.com'); alert('Email copied to clipboard!');" class="btn-copy" aria-label="Copy email to clipboard">📋 Copy</button>
</span>
```

### B. Form Backend Integration
Instead of simulating submissions, map the `action` attribute of the `<form>` tag to a static handler such as **Formspree** or **Netlify Forms**:
```html
<!-- Formspree Endpoint Example -->
<form action="https://formspree.io/f/your-form-id" method="POST" id="contact-form">
```
This requires zero backend coding and guarantees that customer emails land in the developer's inbox.

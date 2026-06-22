# CafePulse Website V1: Community Form Strategy

This report analyzes interaction workflows (Google Forms vs. Email-based systems) for early-stage operations:
- Founder Program signups
- Beta Tester registrations
- Bug submissions
- Feature requests

---

## 1. Google Forms vs. Email Workflows

| Operations Task | Google Forms Workflow | Direct Email Workflow |
| :--- | :--- | :--- |
| **Founder Signups** | **Pros**: Structured data (fields for name, license keys, email). Easily exported to Sheets.<br>**Cons**: Direct payment links must be manually sent afterwards, causing friction. | **Pros**: Creates high-touch direct communication between founder and user.<br>**Cons**: Unstructured; requires manual key tracking. |
| **Beta Tester Signups**| **Pros**: Filters candidates (e.g. asking for OS, router model, network size). Limits access easily.<br>**Cons**: Adds an external redirect. | **Pros**: Simple, zero friction.<br>**Cons**: Messy to filter and track; often misses critical diagnostic details. |
| **Bug Submissions** | **Pros**: Forces submission of crash logs, OS specs, and version details via required inputs.<br>**Cons**: User has to copy-paste. | **Pros**: Flexible attachments (log files, pictures).<br>**Cons**: Missing system specs; harder to parse than structured forms. |
| **Feature Requests** | **Pros**: Allows voting polls or simple structured list aggregation.<br>**Cons**: Feels impersonal. | **Pros**: Deeper feedback and custom suggestions.<br>**Cons**: High volume; hard to categorize. |

---

## 2. Strategic Recommendations for CafePulse Early Phase

For V1/Revision 2.0, we recommend a **hybrid operational strategy** optimized for simplicity and high user engagement:

### 2.1 Founder Signups & Purchases
- **Strategy**: **Email-based / Invoice Workflow**.
- **Execution**: The user sends an email to `cafepulse.network@gmail.com` requesting a Founder key. The team responds with localized invoice instructions (QRIS/Payment links). Upon validation, the license file is emailed back.
- **Why**: Protects the limited 100 slots from spam, and builds personal bonds with early adopters.

### 2.2 Beta Tester Registration
- **Strategy**: **Google Forms** (linked via a clean CTA from `beta.html`).
- **Execution**: Set up a structured Google Form to gather candidate specs (operating system, router models).
- **Why**: Helps filter the target 10 active beta testers to cover different configurations (e.g., Windows vs. Linux, RouterOS v6 vs. v7).

### 2.3 Bug Submissions & Feature Requests
- **Strategy**: **GitHub Issues Integration** (fallback to direct Email).
- **Execution**: Link the "Submit Bug" CTA directly to the repository issues page with pre-populated templates. If the user is non-technical, fallback to direct email instructions.
- **Why**: Encourages developers and network operators to use collaborative public trackers, which builds community trust.

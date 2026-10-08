# LegalIQ | Enterprise Agentic Legal Intelligence

![LegalIQ Logo](legal%20iq.jpeg)

**LegalIQ** is an autonomous, verifiable legal assistant designed for multi-document legal case reasoning, factual grounding, statutory cross-referencing, contradiction detection, and court-ready petition drafting.

---

## ⚖️ Key Features

- **Multi-Document Ingestion & Management:**
  - Drag-and-drop or upload multiple case dossiers (`.txt`, `.pdf`, `.docx`).
  - Active document list with status pills and quick in-app modal document previewer.
  
- **Strict Anti-Hallucination & Relevance Guardrails:**
  - **No File Uploaded:** Prompts the user to upload case files before asking questions.
  - **Off-Topic Detection:** Automatically filters out invalid or unrelated questions, maintaining 100% evidentiary integrity.
  - **Zero Fabrication Gate:** Every response is directly anchored to facts established in the uploaded case dossiers.

- **Automated Contradiction Detection:**
  - Cross-references witness statements against complainant statements.
  - Detects time, venue, and narrative discrepancies (e.g., 10:30 AM vs 03:00 PM meeting conflict).
  - Highlights evidentiary impact under Sections 145 & 155 of the Indian Evidence Act.

- **Court-Ready Legal Drafting:**
  - Instantly formats complete Regular Bail Petitions under **Section 437 Cr.P.C.** / **Section 480 Bharatiya Nagarik Suraksha Sanhita (BNSS)**.
  - Incorporates landmark Supreme Court citations (*Arnesh Kumar*, *Satishchandra Ratanlal Shah*).

- **Real-Time Evaluation Rubric:**
  - Groundedness scoring (up to 98.9%).
  - Retrieval precision metrics.
  - Fabrication checks and conflict tracking.

- **ChatGPT-Style Modern UI:**
  - Sleek dark theme with neon accents and two-column sidebar navigation.
  - One-click copy, quick prompt chips, and verified source citations.

---

## 📁 Repository Structure

```
├── index.html                           # Full standalone interactive LegalIQ dashboard
├── legal iq.jpeg                        # LegalIQ official logo branding
├── Sample_Legal_Case_FIR_42_2023.txt    # Sample benchmark case dossier (FIR 42/2023)
├── app.py                               # Optional Streamlit application
├── requirements.txt                     # Python dependencies
├── run.bat                              # Quick launch batch script for Windows
└── README.md                            # Documentation
```

---

## 🚀 Quick Start

### Option 1: Standalone Web App (Recommended)
Simply open `index.html` in any modern web browser (Google Chrome, Microsoft Edge, Firefox):
1. Double-click `index.html` (or right-click → **Open with** → **Browser**).
2. Upload `Sample_Legal_Case_FIR_42_2023.txt` using the left sidebar upload card.
3. Start asking case questions or click any of the quick action buttons.

### Option 2: Python / Streamlit App
If you wish to run the Streamlit version:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
streamlit run app.py
```

---

## 🛠️ Built With
- **Frontend:** HTML5, Tailwind CSS, FontAwesome 6, Modern Vanilla JavaScript
- **Backend / Python:** Python 3.10+, Streamlit
- **Design:** LegalIQ Custom Design System

---

## 👤 Author
- **GitHub:** [@saransivam24](https://github.com/saransivam24)
- **Repository:** [legal-AI-chatbot-](https://github.com/saransivam24/legal-AI-chatbot-)

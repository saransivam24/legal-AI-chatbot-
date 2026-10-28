# LegalIQ Chatbot ⚖️🤖

An intelligent, AI-powered legal assistant web application designed to analyze legal documents, synthesize complex statutes, and provide interactive contextual guidance with a responsive, modern interface.

---

## 🚀 Overview

**LegalIQ** leverages large language models to assist users with legal inquiries, contract review, and automated documentation. Built with a lightweight Python backend and a responsive dark-themed frontend, it provides instant legal insights and sample PDF generation for reference.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI / LLM Integration:** Google Gemini API
- **Frontend:** HTML5, CSS3, Tailwind CSS, Font Awesome
- **Utilities:** Python-based PDF generation (`FPDF` / `ReportLab`)

---

## 📁 Project Structure

```text
legal/
│── data1.txt              # Domain knowledge base / legal context references
│── data2.txt
│── data3.txt
│── data4.txt
│── generate_sample_pdfs.py # Utility script to generate sample legal documents
│── app.py                 # Core Flask application and API routes
│── index.html             # Chat UI and client-side logic
│── logo.jpeg              # Brand asset
│── .gitignore             # Ignored paths (e.g., .env, virtual environment)
└── README.md              # Project documentation ## ✨ Core Features

### 1. Context-Aware Legal Dialogue
- Conversational interface fine-tuned with domain context prompts to maintain objective, analytical, and jurisdiction-conscious tone.
- Contextual retention across chat sessions with dynamic typing status indicators and streaming token response handling.

### 2. Multi-Tier Knowledge Grounding (RAG-Ready)
- Ingests structured and unstructured knowledge bases (`data1.txt` through `data4.txt`) covering legal definitions, procedural timelines, and reference statutes.
- Prioritizes domain data over raw model hallucinations to ensure references remain grounded.

### 3. Automated Document Generation Engine
- Dedicated document pipeline (`generate_sample_pdfs.py`) to synthesize formal test cases, legal notices, NDAs, and sample briefs into standard PDF structures.

### 4. Sleek, Distraction-Free UI
- Responsive, dark-palette dashboard built with Tailwind CSS utility architecture.
- Real-time client rendering with Font Awesome icons, dynamic DOM mutations, and smooth scroll anchors.

---

## 🏗️ System Architecture

```text
+-----------------------------------------------------------------+
|                         Client Layer                            |
|             (index.html | Tailwind CSS | Dynamic DOM)           |
+-----------------------------------------------------------------+
                                |  (HTTP JSON Requests)
                                v
+-----------------------------------------------------------------+
|                        Flask Backend                            |
|                           (app.py)                              |
+-----------------------------------------------------------------+
           |                                        |
           | (Corpus Ingestion)                     | (API Inference)
           v                                        v
+-----------------------+              +--------------------------+
|  Local Grounding Data |              |     Google Gemini API    |
|   (data1.txt ... 4)   |              |   (gemini-1.5-pro/flash) |
+-----------------------+              +--------------------------+
           |
           +-------------------> [Context Assembly] ---> [Response Payload]

# ⚡ Enterprise Customer Workflow Analyzer

A multi-step customer experience analytics dashboard powered by **Local LLMs** (via **Ollama** and **Qwen2.5**). This application processes customer feedback, extracts actionable insights, detects urgency levels, and drafts personalized customer service responses—all locally with **zero API costs** and **100% data privacy**.

---

## 🌟 Key Features

- **🔒 100% Local & Secure:** Operates entirely offline using Ollama. No customer data leaves your local network.
- **📝 Single Review Analysis:** Instant sentiment detection, key issue extraction, urgency assessment (🚨 High Urgency, ⚠️ Action Required), and automated response drafting.
- **📁 Batch Processing (CSV):** Upload large feedback datasets (CSV format) to automatically analyze and summarize customer input at scale.
- **🎨 Custom Pipeline Controls:** Adjust LLM creativity (`Temperature`), select different local models, and define target customer response tones (e.g., *Empathetic*, *Professional*).
- **📊 Exportable Insights:** Review processing logs and download structured analysis results in CSV format.

---

## 🛠️ Tech Stack

- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **LLM Engine:** [Ollama](https://ollama.com/)
- **Local Model:** [Qwen2.5](https://ollama.com/library/qwen2.5)
- **Data Processing:** Python, Pandas

---

## 🚀 Quick Start

### Prerequisites

1. Install **[Ollama](https://ollama.com/)**.
2. Pull the **Qwen2.5** model via terminal/CMD:
   ```bash
   ollama pull qwen2.5

## 🎬 Video Demo & Walkthrough

Watch the full system demonstration, workflow breakdown, and architecture overview on Google Drive:

[![Watch Project Demo](https://img.shields.io/badge/Google_Drive-Watch_Full_Demo-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)]((https://drive.google.com/file/d/1yVVwlgmNSwVPqULwltH2jUav5C7QQ2yy/view?usp=sharing))

> 💡 **Tip:** You can download `sample_reviews.csv` from this repository to test the **Batch Analysis** feature yourself as shown in the video!

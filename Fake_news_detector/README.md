# Fake News Detection using Bidirectional LSTM

[![Deep Learning](https://img.shields.io/badge/Deep%20Learning-BiLSTM-blue.svg)](https://tensorflow.org)
[![Accuracy](https://img.shields.io/badge/Test%20Accuracy-99.36%25-brightgreen.svg)](https://github.com/m4gnel/PROJECTS)
[![KTU Course](https://img.shields.io/badge/KTU-AIT--401-orange.svg)](https://ktu.edu.in)
[![Frontend](https://img.shields.io/badge/UI-React%20%2B%20Vite%20%2B%20Tailwind%20Dark-purple.svg)](./frontend)

A deep learning fake news detection system developed as part of **AIT-401 – Foundations of Deep Learning** at **Adi Shankara Institute of Engineering and Technology, Kalady** (affiliated with **APJ Abdul Kalam Technological University, Kerala**).

---

## 👥 Project Team & Supervision

- **Krishna Priya V R** — `ASI23CA039`
- **Magnel Olivero** — `ASI23CA040`
- **Miliya Rose Sephy** — `ASI23CA041`
- **Project Guide:** Prof. Asha Rose Thomas (Dept. of AI & DS)
- **Head of Department:** Dr. Sarika S

---

## 🎯 Key Achievements & Architecture

- **Model:** Bidirectional Long Short-Term Memory (BiLSTM) with 64 units each way (128 concatenated bidirectional context units).
- **Parameters:** **2,662,977 parameters** (~10.7 MB at 32-bit float).
- **Dataset:** Kaggle Fake and Real News Dataset (39,100 deduplicated articles, 80/20 stratified split).
- **Test Performance:** **99.36% Test Accuracy** across 7,821 unseen articles (0.99 Precision, 0.99 Recall, 0.99 F1-score).
- **Data Leakage Prevention (CO1):** Removal of the news-agency dateline artifact (`"CITY (Reuters) -"`) from real articles to ensure the neural network learns semantic patterns rather than a dataset shortcut.
- **Explainability (LIME):** Word-level token attribution highlighter exposing which phrases triggered "Fake" cues vs "Credible" cues.

### Confusion Matrix (7,821 Test Articles)

| | Predicted Real | Predicted Fake | Total |
|---|---|---|---|
| **Actual Real** | **4,214** (True Real) | 25 (False Fake) | 4,239 |
| **Actual Fake** | 25 (False Real) | **3,557** (True Fake) | 3,582 |

---

## 💻 Modern Dark UI Frontend (`frontend/`)

The frontend is an ultra-modern dark AI chat and evaluation dashboard inspired by premium conversational interfaces (Perplexity / Claude / ChatGPT style):

- **Collapsible Sidebar:** Featuring the flower emblem, New Chat, Search, Projects list (*Pirnjo 03*, *Meku 02*, *Formbold 04*, *Tailadmin 03*), and user profile card for Magnel Olivero.
- **Center Prompt Card:** Multiline input box with attachment tools, NLP settings, model switcher, and circular submit button.
- **Quick Action Chips:** Deep Search, Saliency Map, Latest News, BiLSTM Neural Flow, and 99.36% Metrics.
- **Interactive Verdict Card:**
  - Real-time prediction badge (`🚨 LIKELY FAKE` / `✅ LIKELY REAL`).
  - Animated confidence progress gauge.
  - 4-step preprocessing inspection stepper.
  - Interactive **LIME Word Attribution Highlighter** with word impact tooltips.
  - Stylometric indicators (Sensationalism, Objectivity, Lexical Diversity).
  - JSON and clipboard export.
- **Built-in Modals:**
  - 📊 **Model Metrics:** Confusion matrix, Epoch 1–4 convergence table.
  - 🧠 **Neural Architecture:** Layer-by-layer parameter inspector and LSTM memory gating formulas.
  - 📑 **Project Report Viewer:** Full in-browser reader of the AIT-401 Course Project Report.
  - 🧪 **Benchmark Samples:** 1-click test cases (e.g., Moon Cheese benchmark, Reuters Senate bill, etc.).

---

## 🚀 Quickstart Guide

### 1. Run the Frontend Web Application

```bash
cd frontend
npm install
npm run dev
```

Open your browser at `http://localhost:5173/`.

To build the static production bundle:
```bash
npm run build
npm run preview
```

### 2. Run the Deep Learning Python Pipeline

```bash
# Install dependencies
pip install pandas numpy scikit-learn nltk tensorflow matplotlib

# Classify a sample article
python fake_news_lstm.py --predict "Breaking: scientists confirm the moon is made of cheese"

# Train on Fake.csv and True.csv
python fake_news_lstm.py --train
```

---

## 📄 Documentation

- Full 29-page Academic Project Report: [`PROJECT_REPORT.md`](./PROJECT_REPORT.md)
- Original Colab Notebook script: [`dl_fakenews_detector.py`](./dl_fakenews_detector.py)
- Standalone Model script: [`fake_news_lstm.py`](./fake_news_lstm.py)

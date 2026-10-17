# 🏆 Amazon ML Challenge — Multimodal Multilingual Entity Resolution System

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue.svg)](#)
[![LightGBM](https://img.shields.io/badge/Model-LightGBM%20GBDT-brightgreen.svg)](#)
[![Embeddings](https://img.shields.io/badge/Embeddings-MPNet%20Multilingual-orange.svg)](#)
[![Metric](https://img.shields.io/badge/Metric-Macro%20F0.5%20Optimized-red.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

A high-throughput, enterprise-scale Machine Learning pipeline designed for **Business Entity Resolution (ER)** across diverse international jurisdictions (US, India, and France). Built to solve the **Amazon ML Challenge**, the system narrows down millions of pairwise comparisons using a 5-strategy union blocking mechanism, extracts 22 semantic, lexical, and structural features, and scores candidate pairs using a calibrated LightGBM classifier specifically tuned for the **precision-weighted $F_{0.5}$ metric**.

---

## 🎯 Problem Statement & Strategy

Business Entity Resolution aims to identify and link records referring to the same real-world business across disparate sources with noise, spelling variations, abbreviations, multilingual diacritics, and missing addresses.

### Strategic Optimization for $F_{0.5}$
Because the competition evaluates on $F_{0.5}$ (where precision is weighted 2× higher than recall):
- **False merges are severely penalized**: Incorrectly linking two distinct businesses hurts the score twice as much as missing a valid link.
- **Conservative Decision Boundaries**: Uncertainty defaults to singleton classification (predicting an empty match list earns a perfect $F_{0.5} = 1.0$).
- **Country-Agnostic Design**: Multilingual sentence embeddings natively generalize to unseen jurisdictions (e.g. France) without hardcoded rules.

---

## 🏗️ Two-Stage Architecture

```
 Raw Data Sources (TSV)
           │
           ▼
 [ Text Normalization ] ────► Unicode NFC, Abbreviation Expansion, Legal Form Handling
           │
           ▼
 [ 5-Stage Union Blocking ] ──► BK-1: TF-IDF (char 2-4 gram) ANN Cosine Similarity
           │                   BK-2: Character Trigram Inverted Index (Jaccard >= 0.2)
           │                   BK-3: (Country, First Token) Exact Match
           │                   BK-4: Soundex Phonetic Key Match
           │                   BK-5: Address Token Overlap (>= 2 common tokens)
           ▼
 [ 22-Feature Engineering ] ──► Lexical: Levenshtein, Jaro-Winkler, Token Sort/Set Ratio
           │                   Semantic: Multilingual MPNet Embedding Cosine Similarity
           │                   Structural: Length delta, token count delta, country match
           ▼
 [ LightGBM Matching Engine ] ─► Gradient Boosted Trees trained on hard negative pairs
           │
           ▼
 [ F0.5 Calibrated Threshold ] ─► Conservative thresholding yielding high-precision clusters
           │
           ▼
 Final Output TSV Submission
```

---

## 📁 Repository Structure

```
amazon_ml_challenge/
├── code/
│   └── business_entity_resolution/
│       ├── requirements.txt       # Core dependencies
│       └── src/
│           ├── blocker.py         # 5-stage candidate generation
│           ├── feature_engineer.py# 22-feature vector extraction
│           ├── matcher.py         # LightGBM classifier & trainer
│           ├── evaluator.py       # Macro F0.5 metric evaluation
│           ├── normalizer.py      # Multilingual text normalization
│           └── run_pipeline.py    # End-to-end pipeline orchestrator
├── configs/
│   ├── config.yaml                # Standard pipeline configuration
│   └── config_scalable.yaml       # Scalable memory-efficient configuration
├── notebooks/                     # Exploratory Data Analysis & visual evaluation
├── blocker_scalable.py            # High-performance chunked candidate blocking
├── run_pipeline_scalable.py       # Scalable pipeline runner with checkpointing
├── fast_predict.py                # Accelerated prediction script for test set
├── test_smart_matcher.py          # Validation evaluation script
├── .gitignore                     # Git ignore rules for datasets, models, and caches
└── README.md                      # Comprehensive documentation
```

---

## 🚀 Quick Start Guide

### 1. Installation
Ensure Python 3.10+ is installed:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r code/business_entity_resolution/requirements.txt
```

### 2. Running Validation & Evaluation
Run the test validation script:
```bash
python test_smart_matcher.py
```

### 3. Running the Full Pipeline
Execute the full training, feature extraction, and prediction pipeline:
```bash
python run_pipeline_scalable.py --config configs/config.yaml
```

---

## 🔒 Security & Data Hygiene

- **Data Privacy**: Raw competition datasets (`dataset/`) and trained model binary weights (`models/*.pkl`) are excluded from Git tracking via `.gitignore`.
- **Reproducibility**: Global random seeds (`seed=42`) ensure deterministic feature splits, model training, and candidate generation.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

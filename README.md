# 🚀 Engineering Projects Portfolio

[![Monorepo Structure](https://img.shields.io/badge/Monorepo-9%20Production--Grade%20Projects-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB.svg?logo=python&logoColor=white)](#)
[![TypeScript / React](https://img.shields.io/badge/Frontend-Next.js%2015%20%7C%20React%2019-000000.svg?logo=react&logoColor=white)](#)
[![Flutter](https://img.shields.io/badge/Mobile-Flutter%203.x%20%7C%20Kotlin-02569B.svg?logo=flutter&logoColor=white)](#)
[![Machine Learning](https://img.shields.io/badge/AI%2FML-LangGraph%20%7C%20LightGBM%20%7C%20PyTorch-FF6F00.svg?logo=pytorch&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

A curated collection of enterprise-grade, competitive software engineering systems spanning **Distributed Multi-Agent Architectures, Machine Learning & Computer Vision, Realtime Multimodal Voice & OS Automation, Mobile Applications, and Full-Stack Cloud Platforms**.

---

## 📑 Portfolio Index

| # | Project | Domain | Primary Tech Stack | Description | Directory |
|---|---|---|---|---|---|
| **1** | **Agri-SAGE** | AgriTech & Decision AI | FastAPI, LangGraph (14 Agents), DSSAT, Kotlin Compose, ONNX | Physics-grounded, multi-agent agricultural intelligence and disease diagnosis platform with statutory chemical safety checks. | [`/AgriSage`](./AgriSage) |
| **2** | **AI Interview Coach** | EdTech & Evaluation AI | Flask, Heuristic/LLM Dual-Engine, Web Speech API, Chart.js | Enterprise technical interview simulator providing real-time voice transcription, STAR scoring, and competency analytics. | [`/Ai_Interview_Coach`](./Ai_Interview_Coach) |
| **3** | **AMRS (Research Scientist)** | Deep Research & Intelligence | FastAPI, Next.js 15, LangGraph, Supabase, Qdrant, Neo4j | Autonomous scientific research platform transforming research inquiries into verified literature reviews, architecture sketches, and roadmaps. | [`/Autonomous Multi-Agent Research Scientist`](./Autonomous%20Multi-Agent%20Research%20Scientist) |
| **4** | **Jarvis AI** | Voice & OS Automation | Python, LiveKit Agents, Gemini 2.0 Live, PyAutoGUI | Duplex real-time multimodal voice assistant capable of autonomous desktop navigation, app management, and persistent vector memory. | [`/J_Code`](./J_Code) |
| **5** | **Zebec AI** | Creator Tools & Publishing | React 19, Express, SQLite, Tailwind CSS | Multi-tenant creator workflow platform for video clip draft generation, review approvals, and social distribution. | [`/Zebec AI`](./Zebec%20AI) |
| **6** | **Amazon ML Challenge** | Big Data & Entity Resolution | Python, LightGBM, MPNet Multilingual Embeddings | High-precision Business Entity Resolution pipeline utilizing 5-stage union blocking and 22 lexical/semantic features tuned for $F_{0.5}$. | [`/amazon_ml_challenge`](./amazon_ml_challenge) |
| **7** | **Flutter Mobile Container** | Mobile Infrastructure | Flutter, Dart, Android SDK, WebView | Production mobile container and device test suite application featuring Material 3 UI and native device diagnostics. | [`/flutter-mobile_container`](./flutter-mobile_container) |
| **8** | **NGO Volunteer Connect** | Social Impact & Community | Flutter, Dart, Material 3, SQLite | Cross-platform community service application facilitating volunteer discovery, initiative rosters, and impact hour verification. | [`/ngo_volunteer_app`](./ngo_volunteer_app) |
| **9** | **Lazy Terminal** | Creative Frontend & Web | Vanilla HTML5, CSS3, JavaScript | Playful Visual Studio Code simulator and interactive parody terminal demonstrating modular front-end UX architecture. | [`/useless_lazy_terminal`](./useless_lazy_terminal) |

---

## 🏛️ Deep-Dive Architecture Overviews

### 1. Agri-SAGE — Multi-Agent Agricultural Guidance Engine
- **Engine**: 14-Agent state machine implemented with LangGraph and FastAPI.
- **Biophysical Modeling**: Direct integration with the DSSAT CSM biophysical crop simulation model for irrigation and yield forecasting.
- **Edge Inference**: EfficientNet-B3 ONNX models running on-device inside a native Kotlin Jetpack Compose Android client.
- **Regulatory Compliance**: Integrated CIB&RC chemical validation engine preventing harmful pesticide recommendations.

### 2. AI Interview Coach — Dual-Engine Mock Interviewer
- **Dual-Engine Evaluation**: Runs a local, deterministic heuristic STAR grader alongside an LLM evaluator (OpenAI v1.0+ / Gemini) with graceful offline fallback.
- **Voice-to-Text**: Real-time duplex speech recognition using native Web Speech APIs with visual audio feedback waveforms.
- **Visual Analytics**: Interactive radar and line charts illustrating progression across System Design, Behavioral, Frontend, and Backend competencies.

### 3. AMRS (Autonomous Multi-Agent Research Scientist)
- **Deep Research Graph**: Coordinated stateful agents for planning, arXiv paper retrieval, claim extraction, adversarial fact-checking, and technical architecture sketching.
- **Hybrid Knowledge Storage**: Relational session tracking in PostgreSQL (Supabase), semantic embeddings in Qdrant Cloud, and concept relationship mapping in Neo4j Aura.
- **Robustness**: Fault-tolerant `ModelRouter` with automated circuit breaking across primary and secondary LLM providers.

### 4. Jarvis AI — Realtime Multimodal Assistant
- **Ultra-Low Latency Audio**: Powered by the LiveKit Agents SDK and Google Gemini 2.0 Multimodal Live Realtime WebSocket API with BVC noise suppression.
- **OS Automation**: Complete window lifecycle control, system volume adjustments, human-like mouse trajectories, and hotkey sequences via PyAutoGUI.
- **Memory Continuity**: Autonomous background memory extraction extracting entities, preferences, and facts into persistent vector storage.

### 5. Zebec AI — Automated Creator Workflow Engine
- **Full-Stack Simplicity**: React 19 UI with Tailwind CSS backed by an Express REST API with Helmet security headers, rate limiting, and JWT authentication.
- **Persistence**: High-throughput SQLite ORM with local write-ahead logging (WAL) support for fast read/write transactions.

### 6. Amazon ML Challenge — Multilingual Entity Resolution
- **5-Stage Blocking**: Union of TF-IDF ANN, character trigram inverted indices, phonetic Soundex keys, and token overlap reducing candidate comparison space by >95%.
- **LightGBM Classification**: 22 lexical, semantic (MPNet), and structural features trained against hard negative pairs.
- **Metric Calibration**: Decision threshold strictly optimized for precision-weighted macro-$F_{0.5}$.

### 7. Flutter Mobile Container
- **Device Diagnostic Container**: Optimized WebView container hosting remote diagnostic suites with animated splash screens and network retry dialogs.
- **Modern Design**: Material 3 design system with custom electric blue theme tokens centrally managed.

### 8. NGO Volunteer Connect
- **Complete Volunteer Flow**: Authentication with personal interest profiling, real-time event browsing, event commitment, and profile impact tracking.
- **Resilient Storage**: Offline-first caching ensuring offline access to registered events and credentials.

### 9. Lazy Terminal
- **Zero-Dependency Web Parody**: Native HTML5, CSS3, and JavaScript simulating the VS Code IDE experience, complete with split panes, terminal window, and quirky conversational humor.

---

## 🔒 Security & Repository Hygiene

This repository enforces strict enterprise security guidelines:
- **Zero Committed Secrets**: All subprojects exclude `.env` files and API keys via the root [`.gitignore`](./.gitignore) and individual project `.gitignore` configurations.
- **Standardized Templates**: Every service requiring external credentials includes a `.env.example` template with clear setup guidance.
- **Database & Build Artifact Exclusion**: Local binary databases (`*.db`, `*.sqlite`), virtual environments (`venv/`, `.venv/`), and frontend builds (`node_modules/`, `.next/`, `build/`) are strictly untracked.

---

## 🚀 Pushing to GitHub

To push all 9 projects into your single GitHub repository (e.g., `projects`):

```powershell
# 1. Initialize root repository
git init

# 2. Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/projects.git

# 3. Stage all files (ensuring submodules are handled cleanly)
git add .

# 4. Commit all 9 projects
git commit -m "feat: initial commit of multi-project engineering portfolio"

# 5. Set main branch and push
git branch -M main
git push -u origin main
```

---

## 📄 License
This repository is licensed under the [MIT License](./LICENSE). Individual projects may also contain domain-specific open-source licenses as documented in their subdirectories.

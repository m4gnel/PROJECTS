# 🎙️ Jarvis AI — Realtime Multimodal Voice & Desktop Automation Agent

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](#)
[![LiveKit](https://img.shields.io/badge/LiveKit-Agents%20SDK-black.svg)](#)
[![Google Gemini](https://img.shields.io/badge/Gemini-2.0%20Multimodal%20Live-8E75B2.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

**Jarvis AI** is an advanced, ultra-low-latency desktop voice assistant and multimodal agent. Engineered with the **LiveKit Agents SDK** and **Google Gemini 2.0 Multimodal Realtime Voice API**, Jarvis enables natural duplex audio conversation combined with autonomous Windows OS control, intelligent web searching, contextual weather synthesis, and persistent semantic long-term memory.

---

## ✨ Core Capabilities

- 🔊 **Duplex Real-Time Voice Streaming**: Ultra-low-latency voice interaction using Google Gemini Realtime (`voice="Charon"`) with DeepFilterNet / BVC background noise cancellation.
- 🖥️ **Full Desktop & Window Automation**:
  - Open, focus, maximize, and terminate desktop applications (`Jarvis_window_CTRL.py`).
  - Native file explorer navigation and media playback (`Jarvis_file_opner.py`).
  - Simulated human-like mouse cursor movements, clicks, scrolling, text typing, hotkeys, and volume controls (`keyboard_mouse_CTRL.py`).
- 🌐 **Live Web & Knowledge Retrieval**:
  - Google Custom Search integration with structured snippet summarization (`Jarvis_google_search.py`).
  - Real-time weather lookup via OpenWeatherMap API (`jarvis_get_whether.py`).
- 🧠 **Long-Term Contextual Memory**:
  - Dynamic memory extraction pipeline storing user preferences, facts, and conversation history (`memory_loop.py`, `memory_store.py`).
  - Semantic vector retrieval ensuring personalized continuity across sessions.

---

## 🏗️ System Architecture

```
                                  [ User Microphone / Speaker ]
                                                │
                                    (WebRTC Audio Stream)
                                                ▼
                                   [ LiveKit Agent Session ]
                                   (BVC Noise Cancellation)
                                                │
                                                ▼
                             [ Google Gemini 2.0 Realtime LLM ]
                                                │
                  ┌─────────────────────────────┼─────────────────────────────┐
                  ▼                             ▼                             ▼
       [ Desktop Automation ]          [ Information Retrieval ]      [ Long-Term Memory ]
       - App Lifecycle Manager         - Google Custom Search         - Memory Extractor
       - Mouse & Keyboard Input        - OpenWeatherMap API           - Vector Storage
       - Window State Controller       - System Clock / Datetime      - Context Injector
```

---

## 📁 Repository Structure

```
J_Code/
├── agent.py                 # LiveKit Agent entrypoint & tool registry
├── Jarvis_prompts.py        # System instructions & persona prompts
├── Jarvis_window_CTRL.py    # Windows OS window management & application launcher
├── Jarvis_file_opner.py     # Local file search & default player integration
├── keyboard_mouse_CTRL.py   # PyAutoGUI mouse, keyboard, and volume controls
├── Jarvis_google_search.py  # Google Custom Search API tool
├── jarvis_get_whether.py    # OpenWeatherMap API tool
├── memory_loop.py           # Background memory extraction logic
├── memory_store.py          # Persistent vector memory repository
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md                # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10, 3.11, or 3.12**
- LiveKit Cloud account (or local LiveKit Server)
- Google Gemini API Key
- Google Custom Search Engine ID & API Key (optional for search)
- OpenWeatherMap API Key (optional for weather)

### 2. Environment Setup
Clone the repository and configure your environment:

```bash
# Copy example environment configuration
cp .env.example .env
```

Edit `.env` with your API keys:
```env
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=wss://your-project.livekit.cloud
GOOGLE_API_KEY=your_google_gemini_api_key
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
SEARCH_ENGINE_ID=your_search_engine_id
OPENWEATHER_API_KEY=your_openweather_api_key
```

### 3. Install Dependencies
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Running the Agent
Start the agent in development mode:
```bash
python agent.py dev
```

Connect using the [LiveKit Agents Playground](https://agents-playground.livekit.io/) or your custom client application.

---

## 🔒 Security & Best Practices

- **API Secrets**: Never commit `.env` or production secrets. The repository is preconfigured with `.gitignore` to prevent credential exposure.
- **Automation Safety**: Mouse and keyboard control utilities incorporate PyAutoGUI fail-safes (moving cursor to any screen corner immediately aborts running automation scripts).
- **Graceful Tool Handling**: All external API calls (weather, search) include structured try/except error boundaries with contextual user feedback.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

# ⚡ Zebec AI — Automated Creator Workflow & Social Publishing Engine

[![React](https://img.shields.io/badge/React-19.2-blue.svg)](#)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B%20%7C%2020%2B-green.svg)](#)
[![Express](https://img.shields.io/badge/Express-4.21-lightgrey.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

**Zebec AI** is a modern, enterprise-ready creator workflow and publishing platform. It empowers content creators and agencies to seamlessly onboard workspaces, select pricing tiers, connect social publishing channels, automatically generate viral clip drafts, orchestrate collaborative approval reviews, and manage multi-platform publishing schedules.

---

## ✨ Features & Architecture

- **Intuitive Creator Onboarding**: Streamlined multi-step onboarding wizard for creator profiles, brand styles, and workspace configuration.
- **Social Channel Integrations**: Unified hub connecting YouTube, TikTok, Instagram, and X/Twitter channels with permission management.
- **AI Clip Draft Generation**: Automated video transcript analysis, hook detection, and clip draft generation pipeline.
- **Review & Approval Gateways**: Granular creator and manager approval workflows with live revision logs before publication.
- **Full-Stack Enterprise Stack**:
  - **Frontend**: Modern React 19 UI with Lucide icons, responsive Tailwind CSS layouts, and smooth micro-interactions.
  - **Backend**: Express REST API with Helmet security headers, CORS protection, rate-limiting, and JWT authentication.
  - **Persistence**: High-performance SQLite ORM with local write-ahead logging (WAL) support.

---

## 🏗️ Architecture Overview

```
 [ React 19 Client ]  <──(Bearer JWT / REST)──>  [ Express 4 API Gateway ]
        │                                                    │
 (Tailwind + Lucide)                              (Helmet + Rate Limiting)
                                                             │
                                                             ▼
                                                    [ SQLite Database ]
                                                (Workspaces, Clips, Users)
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher

### 2. Environment Configuration
Copy the environment templates and configure your settings:

```bash
# Frontend environment
cp .env.example .env

# Backend environment
cp .env.example .env.server
```

**Frontend (`.env`)**:
```env
REACT_APP_API_BASE_URL=http://localhost:5000/api
REACT_APP_ENV=development
REACT_APP_ENABLE_ANALYTICS=false
```

**Backend (`.env.server`)**:
```env
PORT=5000
JWT_SECRET=your-secure-jwt-secret-key-change-in-production
NODE_ENV=development
```

### 3. Installation & Local Development
```bash
# Install dependencies
npm install

# Start both backend and frontend concurrently
npm start
```
- **React Frontend**: http://localhost:3000
- **Express API**: http://localhost:5000/api

---

## 🧪 Testing & Production Build

Run the automated test suite:
```bash
npm test -- --watchAll=false
```

Create an optimized production bundle:
```bash
npm run build
```

---

## 🔒 Security Baseline

- **JWT Authentication**: Secure token verification with bcrypt password hashing.
- **HTTP Protection**: Hardened HTTP headers via `helmet` and strict CORS policy.
- **Rate Limiting**: Automated abuse prevention via `express-rate-limit`.
- **Secret Isolation**: Zero secrets in source control; production variables isolated via environment variables.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

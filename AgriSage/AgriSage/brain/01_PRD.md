# AGRI-SAGE — PRODUCT REQUIREMENTS

## What We Build
Farm decision intelligence for Kerala smallholder farmers. Photo + weather + crop stage + knowledge + simulation → transparent Malayalam advisory. NOT a chatbot.

## Core Loop
Farmer Photo → 14 AI Agents → Cross-Validation → Simulation → Malayalam Advisory → Farmer Acts → System Learns

## Target User
- Kerala smallholder farmer, 0.5–5 ha
- Android phone (2GB RAM minimum, Redmi 10A level)
- Intermittent 2G/4G, Malayalam primary
- No agronomist access

## Launch Crops (V1 — 5 only)
rice | banana | coconut | tomato | maize

## Subscription (Post-Launch)
Free: ₹0, 5 advisories/month
Kisan Basic: ₹49/month, unlimited advisories + offline + alerts
Kisan Pro: ₹149/month, + simulation + schemes + market
Agronomist: ₹499/month, 500 farmer profiles + expert dashboard

## Free Stack
FastAPI + PostgreSQL + pgvector (Oracle Always-Free)
Cline + Gemini API free (aistudio.google.com)
DSSAT BSD-3-Clause | multilingual-e5-large MIT
Firebase FCM free | Cloudflare R2 free 10GB
Razorpay 0 monthly — 2% per transaction only when earning

## MVP for October 1st Demo (Must-Have)
1. Android app opens on real phone
2. OTP registration works
3. Camera with quality indicator
4. ONNX offline disease detection
5. Advisory result in Malayalam
6. Home screen + morning briefing
7. Backend live on Oracle
8. Offline mode works

## Out of Scope — Never Build
Social network | Blockchain | Drone | Autonomous purchasing
Yield guarantees | >5 crops at launch | >4 languages at launch | IoT sensors

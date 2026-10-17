const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');
const { DatabaseSync } = require('node:sqlite');
require('dotenv').config({ path: path.resolve(__dirname, '../.env.server') });

const app = express();
const port = Number(process.env.PORT || 5000);
const jwtSecret = process.env.JWT_SECRET || 'zebec-local-secret-change-me';
const dataDir = path.resolve(__dirname, '../data');

fs.mkdirSync(dataDir, { recursive: true });

const db = new DatabaseSync(path.join(dataDir, 'zebec.db'));
db.exec('PRAGMA journal_mode = WAL;');
db.exec('PRAGMA foreign_keys = ON;');

function initializeDatabase() {
  db.prepare(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      selected_plan TEXT DEFAULT 'starter',
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
  `).run();

  db.prepare(`
    CREATE TABLE IF NOT EXISTS plans (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      price INTEGER NOT NULL,
      clip_limit INTEGER NOT NULL,
      recommended INTEGER NOT NULL DEFAULT 0
    )
  `).run();

  db.prepare(`
    CREATE TABLE IF NOT EXISTS channels (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      platform TEXT NOT NULL,
      handle TEXT NOT NULL,
      subscriber_count INTEGER NOT NULL,
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
  `).run();

  db.prepare(`
    CREATE TABLE IF NOT EXISTS clips (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      title TEXT NOT NULL,
      hook TEXT NOT NULL,
      script TEXT NOT NULL,
      duration_seconds INTEGER NOT NULL,
      approved INTEGER NOT NULL DEFAULT 1,
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
  `).run();

  db.prepare(`
    CREATE TABLE IF NOT EXISTS publish_jobs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      platform TEXT NOT NULL,
      clip_id INTEGER,
      status TEXT NOT NULL DEFAULT 'queued',
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
      FOREIGN KEY (clip_id) REFERENCES clips(id) ON DELETE SET NULL
    )
  `).run();

  const plans = [
    { id: 'starter', name: 'Starter', price: 0, clip_limit: 20, recommended: 0 },
    { id: 'growth', name: 'Growth', price: 19, clip_limit: 120, recommended: 1 },
    { id: 'scale', name: 'Scale', price: 49, clip_limit: 500, recommended: 0 },
  ];

  const insertPlan = db.prepare(`
    INSERT OR IGNORE INTO plans (id, name, price, clip_limit, recommended) VALUES (@id, @name, @price, @clip_limit, @recommended)
  `);

  plans.forEach((plan) => insertPlan.run(plan));
}

initializeDatabase();

function issueToken(user) {
  return jwt.sign({ id: user.id, email: user.email, name: user.name }, jwtSecret, { expiresIn: '7d' });
}

function getUserById(userId) {
  return db.prepare('SELECT * FROM users WHERE id = ?').get(userId);
}

function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization || '';
  const token = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : null;

  if (!token) {
    return res.status(401).json({ message: 'Authentication token required.' });
  }

  try {
    const payload = jwt.verify(token, jwtSecret);
    const user = getUserById(payload.id);

    if (!user) {
      return res.status(401).json({ message: 'User no longer exists.' });
    }

    req.user = { id: user.id, email: user.email, name: user.name, selectedPlan: user.selected_plan };
    next();
  } catch (error) {
    return res.status(401).json({ message: 'Invalid authentication token.' });
  }
}

function normalizeTopic(topic) {
  return String(topic || '').trim();
}

function buildClipDrafts(topic) {
  const safeTopic = normalizeTopic(topic);
  const base = safeTopic.length > 0 ? safeTopic : 'creator growth';

  return [
    {
      title: `${base}: quick hook formula`,
      hook: `Most people overcomplicate ${base}. Here is the shortest path.`,
      script: `Use a simple story arc: problem, proof, payoff. Keep the first sentence sharp and the CTA obvious.`,
      duration_seconds: 32,
      approved: 1,
    },
    {
      title: `${base}: myth to avoid`,
      hook: `The biggest mistake in ${base} is chasing volume without clarity.`,
      script: `Focus on one promise, one audience, and one measurable action. That is what compounds over time.`,
      duration_seconds: 45,
      approved: 1,
    },
    {
      title: `${base}: 3-step action plan`,
      hook: `If you want better results in ${base}, follow the sequence below.`,
      script: `Step one: build a clear insight. Step two: package it into a sharp, relatable story. Step three: repeat it with proof.`,
      duration_seconds: 27,
      approved: 1,
    },
  ];
}

function normalizeClipCandidate(clip) {
  const title = String(clip?.title || 'Untitled clip').trim();
  const hook = String(clip?.hook || 'A sharp opening hook for this topic.').trim();
  const script = String(clip?.script || 'Use a clear value-first explanation and CTA.').trim();
  const duration = Number(clip?.duration_seconds || clip?.durationSeconds || 30);

  return {
    title: title || 'Untitled clip',
    hook: hook || 'A sharp opening hook for this topic.',
    script: script || 'Use a clear value-first explanation and CTA.',
    duration_seconds: Number.isFinite(duration) && duration > 0 ? Math.min(Math.max(Math.round(duration), 15), 90) : 30,
    approved: clip?.approved === false ? 0 : 1,
  };
}

function parseJsonFromText(text) {
  if (!text) return null;

  const candidate = text.includes('{') ? text.slice(text.indexOf('{'), text.lastIndexOf('}') + 1) : text;
  try {
    const parsed = JSON.parse(candidate);
    return parsed;
  } catch (error) {
    const fallback = text.match(/\{[\s\S]*\}/);
    if (!fallback) return null;
    try {
      return JSON.parse(fallback[0]);
    } catch (fallbackError) {
      return null;
    }
  }
}

async function generateOpenAiClips(topic) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) return null;

  const prompt = `Generate 3 short-form video concepts for: ${topic}. Return valid JSON only in this schema: {"clips":[{"title":"...","hook":"...","script":"...","duration_seconds":30}]}. Keep each script concise and engaging.`;

  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: 'You are a short-form content strategist. Return only valid JSON.' },
        { role: 'user', content: prompt },
      ],
      temperature: 0.8,
    }),
  });

  if (!response.ok) {
    throw new Error('OpenAI request failed.');
  }

  const payload = await response.json();
  const text = payload.choices?.[0]?.message?.content;
  const parsed = parseJsonFromText(text);
  if (!parsed || !Array.isArray(parsed.clips)) {
    return null;
  }

  return parsed.clips.map(normalizeClipCandidate);
}

async function generateGeminiClips(topic) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return null;

  const prompt = `Generate 3 short-form video concepts for: ${topic}. Return valid JSON only in this format: {"clips":[{"title":"...","hook":"...","script":"...","duration_seconds":30}]}. Keep content clear and punchy.`;

  const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
    }),
  });

  if (!response.ok) {
    throw new Error('Gemini request failed.');
  }

  const payload = await response.json();
  const text = payload.candidates?.[0]?.content?.parts?.[0]?.text;
  const parsed = parseJsonFromText(text);
  if (!parsed || !Array.isArray(parsed.clips)) {
    return null;
  }

  return parsed.clips.map(normalizeClipCandidate);
}

async function generateAiClips(topic) {
  const providers = [generateOpenAiClips, generateGeminiClips];

  for (const provider of providers) {
    try {
      const result = await provider(topic);
      if (result && result.length > 0) {
        return result;
      }
    } catch (error) {
      console.warn('AI provider failed, falling back locally.', error.message);
    }
  }

  return buildClipDrafts(topic);
}

const api = express.Router();

api.get('/health', (req, res) => {
  res.json({ ok: true, message: 'Zebec AI API is healthy.', timestamp: new Date().toISOString() });
});

api.post('/auth/register', (req, res) => {
  const { name, email, password } = req.body || {};
  const normalizedName = String(name || '').trim();
  const normalizedEmail = String(email || '').trim().toLowerCase();
  const normalizedPassword = String(password || '');

  if (!normalizedName || normalizedName.length < 2) {
    return res.status(400).json({ message: 'Name must be at least 2 characters.' });
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizedEmail)) {
    return res.status(400).json({ message: 'A valid email is required.' });
  }

  if (normalizedPassword.length < 8) {
    return res.status(400).json({ message: 'Password must be at least 8 characters.' });
  }

  const existing = db.prepare('SELECT id FROM users WHERE email = ?').get(normalizedEmail);
  if (existing) {
    return res.status(409).json({ message: 'An account with this email already exists.' });
  }

  const passwordHash = bcrypt.hashSync(normalizedPassword, 12);
  const result = db.prepare('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)').run(normalizedName, normalizedEmail, passwordHash);
  const user = db.prepare('SELECT id, name, email, selected_plan FROM users WHERE id = ?').get(result.lastInsertRowid);
  const token = issueToken(user);

  return res.status(201).json({
    token,
    user: { id: user.id, name: user.name, email: user.email, selectedPlan: user.selected_plan },
  });
});

api.post('/auth/login', (req, res) => {
  const { email, password } = req.body || {};
  const normalizedEmail = String(email || '').trim().toLowerCase();
  const normalizedPassword = String(password || '');

  if (!normalizedEmail || !normalizedPassword) {
    return res.status(400).json({ message: 'Email and password are required.' });
  }

  const user = db.prepare('SELECT * FROM users WHERE email = ?').get(normalizedEmail);
  if (!user) {
    return res.status(401).json({ message: 'Invalid email or password.' });
  }

  const passwordMatches = bcrypt.compareSync(normalizedPassword, user.password_hash);
  if (!passwordMatches) {
    return res.status(401).json({ message: 'Invalid email or password.' });
  }

  const token = issueToken(user);
  return res.json({
    token,
    user: { id: user.id, name: user.name, email: user.email, selectedPlan: user.selected_plan },
  });
});

api.get('/me', authMiddleware, (req, res) => {
  res.json({ user: req.user });
});

api.get('/plans', (req, res) => {
  const plans = db.prepare('SELECT * FROM plans ORDER BY price ASC').all();
  res.json({ plans });
});

api.post('/plans/select', authMiddleware, (req, res) => {
  const { planId } = req.body || {};
  const plan = db.prepare('SELECT * FROM plans WHERE id = ?').get(planId);

  if (!plan) {
    return res.status(400).json({ message: 'Unknown plan selected.' });
  }

  db.prepare('UPDATE users SET selected_plan = ? WHERE id = ?').run(plan.id, req.user.id);
  res.json({ message: 'Plan updated successfully.', selectedPlan: plan.id });
});

api.get('/channels', authMiddleware, (req, res) => {
  const channels = db.prepare(
    'SELECT id, platform, handle, subscriber_count, created_at FROM channels WHERE user_id = ? ORDER BY created_at DESC'
  ).all(req.user.id);
  res.json({ channels });
});

api.post('/channels', authMiddleware, (req, res) => {
  const { platform, handle, subscriberCount } = req.body || {};
  const safePlatform = String(platform || '').trim().toLowerCase();
  const safeHandle = String(handle || '').trim();
  const parsedSubscribers = Number(subscriberCount || 0);

  if (!['youtube', 'instagram', 'tiktok', 'x'].includes(safePlatform)) {
    return res.status(400).json({ message: 'Unsupported platform.' });
  }

  if (!safeHandle || !safeHandle.startsWith('@') || safeHandle.length < 2) {
    return res.status(400).json({ message: 'Channel handle must begin with @ and be at least 2 characters long.' });
  }

  if (!Number.isFinite(parsedSubscribers) || parsedSubscribers < 0) {
    return res.status(400).json({ message: 'Subscriber count must be a non-negative number.' });
  }

  const result = db.prepare(
    'INSERT INTO channels (user_id, platform, handle, subscriber_count) VALUES (?, ?, ?, ?)'
  ).run(req.user.id, safePlatform, safeHandle, Math.floor(parsedSubscribers));

  const channel = db.prepare('SELECT * FROM channels WHERE id = ?').get(result.lastInsertRowid);
  res.status(201).json({ channel });
});

api.get('/clips', authMiddleware, (req, res) => {
  const clips = db.prepare(
    'SELECT id, title, hook, script, duration_seconds, approved, created_at FROM clips WHERE user_id = ? ORDER BY created_at DESC'
  ).all(req.user.id);
  res.json({ clips });
});

api.post('/clips/generate', authMiddleware, async (req, res) => {
  const topic = normalizeTopic(req.body?.topic);

  if (topic.length < 3) {
    return res.status(400).json({ message: 'Topic must be at least 3 characters.' });
  }

  const drafts = await generateAiClips(topic);

  const insertClip = db.prepare(`
    INSERT INTO clips (user_id, title, hook, script, duration_seconds, approved)
    VALUES (?, ?, ?, ?, ?, ?)
  `);

  const stored = drafts.map((draft) => {
    const normalizedDraft = normalizeClipCandidate(draft);
    const result = insertClip.run(
      req.user.id,
      normalizedDraft.title,
      normalizedDraft.hook,
      normalizedDraft.script,
      normalizedDraft.duration_seconds,
      normalizedDraft.approved
    );
    return db.prepare('SELECT * FROM clips WHERE id = ?').get(result.lastInsertRowid);
  });

  return res.status(201).json({ clips: stored });
});

api.patch('/clips/:id/approve', authMiddleware, (req, res) => {
  const clipId = Number(req.params.id);
  const approved = req.body?.approved === true ? 1 : 0;

  const existing = db.prepare('SELECT id FROM clips WHERE id = ? AND user_id = ?').get(clipId, req.user.id);
  if (!existing) {
    return res.status(404).json({ message: 'Clip not found.' });
  }

  db.prepare('UPDATE clips SET approved = ? WHERE id = ?').run(approved, clipId);
  const clip = db.prepare('SELECT * FROM clips WHERE id = ?').get(clipId);
  res.json({ clip });
});

api.post('/publish', authMiddleware, (req, res) => {
  const platforms = Array.isArray(req.body?.platforms) && req.body.platforms.length > 0 ? req.body.platforms : ['youtube'];
  const approvedClips = db.prepare('SELECT id FROM clips WHERE user_id = ? AND approved = 1 ORDER BY created_at DESC').all(req.user.id);

  if (approvedClips.length === 0) {
    return res.status(400).json({ message: 'At least one approved clip is required before publishing.' });
  }

  const rows = platforms.map((platform) => {
    const clipId = approvedClips[0]?.id;
    const result = db.prepare(
      'INSERT INTO publish_jobs (user_id, platform, clip_id, status) VALUES (?, ?, ?, ?)' 
    ).run(req.user.id, String(platform).trim().toLowerCase(), clipId, 'queued');
    return { id: result.lastInsertRowid, platform: String(platform).trim().toLowerCase(), clipId, status: 'queued' };
  });

  res.status(201).json({ message: 'Publishing queue created.', jobs: rows, approvedClipCount: approvedClips.length });
});

const apiRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 200,
  standardHeaders: true,
  legacyHeaders: false,
  message: { message: 'Too many requests. Please wait a moment and try again.' },
});

app.use(cors({ origin: true, credentials: true }));
app.use(helmet({ crossOriginResourcePolicy: { policy: 'cross-origin' } }));
app.use(express.json({ limit: '1mb' }));
app.use(morgan('dev'));
app.use('/api', apiRateLimit);
app.use('/api', api);

if (process.env.NODE_ENV === 'production') {
  const buildDir = path.resolve(__dirname, '../build');
  app.use(express.static(buildDir));
  app.get('*', (req, res, next) => {
    if (req.path.startsWith('/api')) {
      return next();
    }
    res.sendFile(path.join(buildDir, 'index.html'));
  });
}

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ message: 'Internal server error.' });
});

app.listen(port, () => {
  console.log(`Zebec AI API running on http://localhost:${port}`);
});

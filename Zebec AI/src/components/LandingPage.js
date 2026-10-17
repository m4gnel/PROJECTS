import React from 'react';
import { ArrowRight, BarChart3, ShieldCheck, Sparkles, TrendingUp, Wand2, Zap } from 'lucide-react';

const STATS = [
  { label: 'Avg. turnaround', value: '3.2x faster' },
  { label: 'Clips generated', value: '120+/mo' },
  { label: 'Uptime', value: '99.9%' },
];

const FEATURES = [
  { icon: Wand2, title: 'AI-powered concepting', text: 'Turn any topic into hooks, scripts, and thumbnail-ready angles in seconds.' },
  { icon: BarChart3, title: 'Live creator analytics', text: 'Track channel performance, reach, and publish momentum from one dashboard.' },
  { icon: ShieldCheck, title: 'Secure by default', text: 'Built with safe auth, token handling, and a production-minded workflow.' },
  { icon: Zap, title: 'One-click publishing', text: 'Approve, schedule, and push content to top social platforms without friction.' },
];

export default function LandingPage({ navigate }) {
  return (
    <main className="page home-page">
      <section className="card hero hero-panel">
        <div className="hero-copy">
          <div className="eyebrow">
            <Sparkles size={16} />
            Creator growth system
          </div>
          <h1>
            Launch short-form content <span className="gradient-text">faster</span> with Zebec AI
          </h1>
          <p>
            An execution platform for creators and teams: connect channels, generate high-converting clips, review output, and publish with confidence.
          </p>

          <div className="actions">
            <button type="button" className="primary-button" onClick={() => navigate('auth')}>
              Get started for free
              <ArrowRight size={16} />
            </button>
            <button type="button" className="ghost-button" onClick={() => navigate('plans')}>
              View plans
            </button>
          </div>

          <div className="mini-metrics">
            {STATS.map((stat) => (
              <div key={stat.label} className="metric-card">
                <strong>{stat.value}</strong>
                <span>{stat.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="hero-visual" aria-label="Product overview preview">
          <div className="visual-window">
            <div className="window-head">
              <span className="dot red" />
              <span className="dot yellow" />
              <span className="dot green" />
            </div>

            <div className="window-body">
              <div className="visual-card success">
                <TrendingUp size={18} />
                <div>
                  <small>Campaign health</small>
                  <strong>+32% engagement</strong>
                </div>
              </div>

              <div className="visual-stack">
                <div className="visual-line highlight" />
                <div className="visual-line" />
                <div className="visual-line" />
                <div className="visual-line short" />
              </div>

              <div className="content-pills">
                <span>Hook</span>
                <span>Script</span>
                <span>Publish</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="feature-grid" aria-label="Platform advantages">
        {FEATURES.map(({ icon: Icon, title, text }) => (
          <article key={title} className="feature-card">
            <div className="feature-icon">
              <Icon size={18} />
            </div>
            <h3>{title}</h3>
            <p>{text}</p>
          </article>
        ))}
      </section>
    </main>
  );
}

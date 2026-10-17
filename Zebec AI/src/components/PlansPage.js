import React from 'react';

const PLANS = [
  {
    id: 'starter',
    name: 'Starter',
    price: '$0',
    clips: '20 clips / month',
    summary: 'For new creators validating their first audience.',
    features: ['1 channel link', 'AI brief generation', 'Basic publishing queue'],
  },
  {
    id: 'growth',
    name: 'Growth',
    price: '$19',
    clips: '120 clips / month',
    summary: 'For consistent creators building momentum every week.',
    recommended: true,
    features: ['Unlimited campaign ideas', 'Multi-platform publishing', 'Priority AI optimization'],
  },
  {
    id: 'scale',
    name: 'Scale',
    price: '$49',
    clips: '500 clips / month',
    summary: 'For teams and agencies scaling output without chaos.',
    features: ['Team workspace', 'Analytics snapshots', 'Advanced scheduling & reporting'],
  },
];

export default function PlansPage({ handlePlanSelect, selectedPlan }) {
  return (
    <main className="page">
      <section className="card product-panel">
        <div className="section-header center-header">
          <p className="eyebrow compact">Pricing built to scale</p>
          <h2>Choose the plan that matches your growth engine</h2>
        </div>

        <div className="grid plan-grid">
          {PLANS.map((plan) => (
            <article key={plan.id} className={`plan-card ${selectedPlan?.id === plan.id ? 'is-selected' : ''}`}>
              {plan.recommended ? <p className="pill">Most popular</p> : null}
              <div className="plan-head">
                <h3>{plan.name}</h3>
                <p className="price">{plan.price}<span>/mo</span></p>
              </div>
              <p className="plan-clips">{plan.clips}</p>
              <p className="muted plan-summary">{plan.summary}</p>

              <ul className="feature-list">
                {plan.features.map((feature) => (
                  <li key={feature}>{feature}</li>
                ))}
              </ul>

              <button type="button" className="primary-button" onClick={() => handlePlanSelect(plan.id)}>
                {selectedPlan?.id === plan.id ? 'Selected' : 'Select plan'}
              </button>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

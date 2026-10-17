import React from 'react';

export default function SuccessPage({
  userData,
  selectedPlan,
  linkedChannels,
  connectedPlatforms,
  approvedClipCount,
  handleReset,
  navigate,
}) {
  return (
    <main className="page">
      <section className="card product-panel success-panel">
        <div className="success-badge">Campaign launched</div>
        <h2>Publishing pipeline is ready</h2>
        <p>
          Great work {userData?.name}. Your workspace is configured and your next batch is ready to ship.
        </p>

        <ul className="result-list result-grid">
          <li><span>Plan</span> {selectedPlan?.name}</li>
          <li><span>Channels</span> {linkedChannels.length}</li>
          <li><span>Platforms</span> {connectedPlatforms.length}</li>
          <li><span>Approved</span> {approvedClipCount}</li>
        </ul>

        <div className="actions">
          <button type="button" className="ghost-button" onClick={() => navigate('dashboard')}>
            Back to studio
          </button>
          <button type="button" className="primary-button" onClick={handleReset}>
            Reset workspace
          </button>
        </div>
      </section>
    </main>
  );
}

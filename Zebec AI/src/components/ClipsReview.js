import React from 'react';

export default function ClipsReview({
  clips,
  approvedClipCount,
  handleClipApprovalToggle,
  navigate,
}) {
  return (
    <main className="page">
      <section className="card product-panel review-panel">
        <div className="section-header">
          <div>
            <p className="eyebrow compact">Review board</p>
            <h2>Approve the winning cuts</h2>
          </div>
          <span className="small-badge">{approvedClipCount} ready</span>
        </div>

        <div className="stack clip-stack">
          {clips.map((clip) => (
            <article key={clip.id} className="clip-card">
              <div className="clip-topline">
                <h3>{clip.title}</h3>
                <span>{clip.durationSeconds}s</span>
              </div>
              <p><strong>Hook:</strong> {clip.hook}</p>
              <p><strong>Script:</strong> {clip.script}</p>
              <button
                type="button"
                className={clip.approved ? 'ghost-button' : 'primary-button'}
                onClick={() => handleClipApprovalToggle(clip.id)}
              >
                {clip.approved ? 'Mark as draft' : 'Approve clip'}
              </button>
            </article>
          ))}
        </div>

        <button type="button" className="primary-button" onClick={() => navigate('social-connect')}>
          Continue to social publishing
        </button>
      </section>
    </main>
  );
}

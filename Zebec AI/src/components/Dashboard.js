import React, { useState } from 'react';

export default function Dashboard({ linkedChannels, clips, handleClipsGenerated, navigate }) {
  const [topic, setTopic] = useState('');
  const [error, setError] = useState('');

  const onGenerate = async (event) => {
    event.preventDefault();
    const normalizedTopic = topic.trim();
    if (normalizedTopic.length < 3) {
      setError('Topic must be at least 3 characters.');
      return;
    }
    setError('');
    const result = await handleClipsGenerated({ topic: normalizedTopic });
    if (!result || !result.ok) {
      setError(result?.message || 'Unable to generate clips right now.');
    }
  };

  return (
    <main className="page">
      <section className="card product-panel dashboard-panel">
        <div className="section-header">
          <div>
            <p className="eyebrow compact">Creator studio</p>
            <h2>Build your next content signal</h2>
          </div>
          <span className="small-badge">{linkedChannels.length} channels live</span>
        </div>

        <div className="dashboard-layout">
          <div className="studio-form-wrap">
            <form onSubmit={onGenerate} noValidate>
              <label htmlFor="topic-input">Campaign topic</label>
              <input
                id="topic-input"
                type="text"
                placeholder="e.g., building a high-converting personal brand"
                value={topic}
                onChange={(event) => setTopic(event.target.value)}
              />
              {error ? <p className="error-text">{error}</p> : null}
              <button type="submit" className="primary-button">Generate clip drafts</button>
            </form>

            {clips.length > 0 ? (
              <button type="button" className="ghost-button" onClick={() => navigate('clips-review')}>
                Review existing drafts ({clips.length})
              </button>
            ) : null}
          </div>

          <aside className="dashboard-side">
            <div className="summary-block">
              <h3>Connected channels</h3>
              <ul>
                {linkedChannels.map((channel) => (
                  <li key={channel.id}><span>{channel.platform}</span> {channel.name}</li>
                ))}
              </ul>
            </div>

            <div className="summary-block spotlight">
              <h3>Content flywheel</h3>
              <div className="mini-flow">
                <span>Hook</span>
                <span>Script</span>
                <span>Publish</span>
              </div>
            </div>
          </aside>
        </div>
      </section>
    </main>
  );
}

import React from 'react';

const PLATFORMS = ['youtube', 'instagram', 'tiktok', 'x'];

export default function SocialConnect({
  connectedPlatforms,
  handlePlatformConnect,
  approvedClipCount,
  handlePublish,
}) {
  return (
    <main className="page">
      <section className="card product-panel social-panel">
        <div className="section-header">
          <div>
            <p className="eyebrow compact">Publishing</p>
            <h2>Choose your distribution network</h2>
          </div>
        </div>

        <div className="grid platform-grid">
          {PLATFORMS.map((platform) => {
            const isConnected = connectedPlatforms.includes(platform);
            return (
              <button
                key={platform}
                type="button"
                className={`platform-button ${isConnected ? 'is-active' : ''}`}
                onClick={() => handlePlatformConnect(platform)}
              >
                <span className="platform-name">{platform}</span>
                <span className="platform-state">{isConnected ? 'connected' : 'connect'}</span>
              </button>
            );
          })}
        </div>

        <button
          type="button"
          className="primary-button"
          disabled={connectedPlatforms.length === 0 || approvedClipCount === 0}
          onClick={handlePublish}
        >
          Publish {approvedClipCount} approved clips
        </button>
      </section>
    </main>
  );
}

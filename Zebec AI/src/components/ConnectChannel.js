import React, { useState } from 'react';

const CHANNELS = ['youtube', 'instagram', 'tiktok'];

export default function ConnectChannel({ handleChannelLink, linkedChannels }) {
  const [platform, setPlatform] = useState(CHANNELS[0]);
  const [handle, setHandle] = useState('@');
  const [subscribers, setSubscribers] = useState('1000');
  const [error, setError] = useState('');

  const onSubmit = async (event) => {
    event.preventDefault();
    const normalizedHandle = handle.trim();
    if (normalizedHandle.length < 2 || !normalizedHandle.startsWith('@')) {
      setError('Handle must start with @ and include at least 2 characters.');
      return;
    }
    if (!/^\d+$/.test(subscribers.trim())) {
      setError('Subscriber count should contain numbers only.');
      return;
    }
    setError('');
    const result = await handleChannelLink({
      platform,
      handle: normalizedHandle,
      subscribers: Number(subscribers.trim()),
    });
    if (!result || !result.ok) {
      setError(result?.message || 'Unable to connect this channel right now.');
    }
  };

  return (
    <main className="page">
      <section className="card product-panel channel-panel">
        <div className="section-header">
          <div>
            <p className="eyebrow compact">Distribution</p>
            <h2>Connect your creator channels</h2>
          </div>
        </div>

        <div className="channel-layout">
          <form onSubmit={onSubmit} noValidate>
            <label htmlFor="platform-select">Platform</label>
            <select id="platform-select" value={platform} onChange={(event) => setPlatform(event.target.value)}>
              {CHANNELS.map((channel) => (
                <option key={channel} value={channel}>{channel}</option>
              ))}
            </select>

            <label htmlFor="handle-input">Channel handle</label>
            <input id="handle-input" type="text" value={handle} onChange={(event) => setHandle(event.target.value)} />

            <label htmlFor="subscribers-input">Subscribers / followers</label>
            <input
              id="subscribers-input"
              type="text"
              inputMode="numeric"
              value={subscribers}
              onChange={(event) => setSubscribers(event.target.value)}
            />

            {error ? <p className="error-text">{error}</p> : null}
            <button type="submit" className="primary-button">Save and continue</button>
          </form>

          {linkedChannels.length > 0 ? (
            <div className="summary-block">
              <h3>Connected channels</h3>
              <ul>
                {linkedChannels.map((channel) => (
                  <li key={channel.id}><span>{channel.platform}</span> {channel.name}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      </section>
    </main>
  );
}

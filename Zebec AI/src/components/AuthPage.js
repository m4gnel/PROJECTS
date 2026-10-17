import React, { useState } from 'react';

export default function AuthPage({ handleLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const onSubmit = async (event) => {
    event.preventDefault();
    const normalizedEmail = email.trim().toLowerCase();
    const normalizedName = name.trim();

    if (!normalizedName) {
      setError('Name is required.');
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizedEmail)) {
      setError('Please enter a valid email address.');
      return;
    }
    if (password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }

    setError('');
    const result = await handleLogin({ email: normalizedEmail, name: normalizedName, password });
    if (!result || !result.ok) {
      setError(result?.message || 'Authentication failed. Please try again.');
    }
  };

  return (
    <main className="page">
      <section className="card auth-panel">
        <div className="auth-layout">
          <div className="auth-copy">
            <p className="eyebrow compact">Why creators choose Zebec AI</p>
            <h2>Create your Zebec AI workspace</h2>
            <ul className="check-list">
              <li>Launch faster with AI-generated hooks and scripts</li>
              <li>Keep channel and publishing workflows in one place</li>
              <li>Move from idea to publish-ready content with confidence</li>
            </ul>
          </div>

          <div className="auth-form-wrap">
            <form onSubmit={onSubmit} noValidate>
              <label htmlFor="name-input">Name</label>
              <input
                id="name-input"
                type="text"
                autoComplete="name"
                value={name}
                onChange={(event) => setName(event.target.value)}
                required
              />
              <label htmlFor="email-input">Email</label>
              <input
                id="email-input"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
              <label htmlFor="password-input">Password</label>
              <input
                id="password-input"
                type="password"
                autoComplete="new-password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
              {error ? <p className="error-text">{error}</p> : null}
              <button type="submit" className="primary-button">Continue</button>
            </form>
          </div>
        </div>
      </section>
    </main>
  );
}

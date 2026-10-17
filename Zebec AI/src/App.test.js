import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

test('renders launch heading', () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: /Launch short-form content/i })).toBeInTheDocument();
});

test('allows user to move from landing to auth', async () => {
  render(<App />);
  await userEvent.click(screen.getByRole('button', { name: /Get started for free/i }));
  expect(screen.getByRole('heading', { name: /Create your Zebec AI workspace/i })).toBeInTheDocument();
});

import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders StyleSense.AI title', () => {
  render(<App />);
  const titleElement = screen.getByText(/StyleSense.AI/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders navigation', () => {
  render(<App />);
  expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
  expect(screen.getByText(/Wardrobe/i)).toBeInTheDocument();
  expect(screen.getByText(/Recommendations/i)).toBeInTheDocument();
});

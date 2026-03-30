import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App.jsx'

describe('App shell', () => {
  it('renders the root calendar shell layout', () => {
    render(<App />)

    expect(screen.getByTestId('app-shell')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: /calendar console/i })).toBeInTheDocument()
  })

  it('renders the core layout regions', () => {
    const { container } = render(<App />)

    expect(container.querySelector('[aria-label="calendar region"]')).not.toBeNull()
    expect(container.querySelector('[aria-label="detail panel"]')).not.toBeNull()
    expect(container.querySelector('[aria-label="execution feed"]')).not.toBeNull()
    expect(screen.getAllByRole('heading', { name: /monday, march 30/i }).length).toBeGreaterThan(0)
  })
})

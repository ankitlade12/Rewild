import { render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import Dashboard from '../Dashboard'

describe('Dashboard', () => {
  const profile = {
    zip_code: '75254',
    area_sqft: 1000,
    current_state: 'maintained_lawn',
    sun_exposure: 'full',
    soil_type: 'well_drained',
    goals: ['pollinators'],
    selectedInterventions: ['native_meadow'],
    locationData: {
      zone: '8a',
      ecoregion: 'Great Plains',
    },
  }

  beforeEach(() => {
    globalThis.fetch = vi.fn()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows simulation error details when API returns non-OK', async () => {
    globalThis.fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Sim failure detail' }),
    })

    render(
      <Dashboard
        profile={profile}
        onBack={vi.fn()}
        onGetActionPlan={vi.fn()}
      />
    )

    expect(await screen.findByRole('heading', { name: /simulation error/i })).toBeInTheDocument()
    expect(screen.getByText(/sim failure detail/i)).toBeInTheDocument()
  })

  it('shows no-scenarios error when API returns empty scenarios', async () => {
    globalThis.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ scenarios: [] }),
    })

    render(
      <Dashboard
        profile={profile}
        onBack={vi.fn()}
        onGetActionPlan={vi.fn()}
      />
    )

    expect(await screen.findByRole('heading', { name: /no scenarios returned/i })).toBeInTheDocument()
    expect(screen.getByText(/try selecting at least one intervention/i)).toBeInTheDocument()
  })
})

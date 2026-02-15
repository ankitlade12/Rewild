import { render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import InterventionPanel from '../InterventionPanel'

describe('InterventionPanel', () => {
  const profile = {
    area_sqft: 1000,
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

  it('shows an explicit error state when lookup fetch fails', async () => {
    globalThis.fetch
      .mockResolvedValueOnce({ ok: true, json: async () => ({ interventions: [] }) })
      .mockResolvedValueOnce({ ok: false, json: async () => ({ detail: 'plants failed' }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ pollinators: [] }) })

    render(
      <InterventionPanel
        profile={profile}
        onBack={vi.fn()}
        onRunSimulation={vi.fn()}
      />
    )

    expect(await screen.findByRole('heading', { name: /data load error/i })).toBeInTheDocument()
    expect(screen.getByText(/failed to load intervention data/i)).toBeInTheDocument()
  })
})

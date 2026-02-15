import { render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import ActionPlan from '../ActionPlan'

describe('ActionPlan', () => {
  const profile = {
    zip_code: '75254',
    area_sqft: 1000,
    sun_exposure: 'full',
    soil_type: 'well_drained',
  }

  beforeEach(() => {
    globalThis.fetch = vi.fn()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows an explicit error state when action-plan API fails', async () => {
    globalThis.fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Action plan failed' }),
    })

    render(
      <ActionPlan
        profile={profile}
        intervention="native_meadow"
        onBack={vi.fn()}
      />
    )

    expect(await screen.findByRole('heading', { name: /action plan error/i })).toBeInTheDocument()
    expect(screen.getByText(/action plan failed/i)).toBeInTheDocument()
  })
})

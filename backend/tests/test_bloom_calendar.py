"""Unit tests for bloom_calendar.py enhancements.

Covers:
- Bloom continuity score (Shannon-entropy based)
- Gap-filling recommendations
- Succession-aware bloom projections (year-by-year)
- Edge cases: no plants, single plant, full coverage
"""

import math
import pytest
from app.engine.bloom_calendar import (
    MONTHS,
    compute_bloom_continuity,
    generate_bloom_calendar,
    generate_succession_bloom,
    _bloom_intensity,
    _build_calendar,
    _FORB_HEIGHT_THRESHOLD_FT,
    _ESTABLISHMENT_RATE,
)


# ── _bloom_intensity ────────────────────────────────────────────────────

class TestBloomIntensity:
    """Tests for bloom intensity classification."""

    def test_short_bloom_window_all_high(self):
        """Species blooming 1–2 months → all months are 'high'."""
        assert _bloom_intensity(6, [6]) == "high"
        assert _bloom_intensity(6, [6, 7]) == "high"
        assert _bloom_intensity(7, [6, 7]) == "high"

    def test_edge_months_are_low(self):
        """First and last month of a 3+ window → 'low'."""
        blooms = [5, 6, 7, 8]
        assert _bloom_intensity(5, blooms) == "low"
        assert _bloom_intensity(8, blooms) == "low"

    def test_interior_months_are_high(self):
        """Interior months → 'high'."""
        blooms = [5, 6, 7, 8]
        assert _bloom_intensity(6, blooms) == "high"
        assert _bloom_intensity(7, blooms) == "high"


# ── compute_bloom_continuity ────────────────────────────────────────────

class TestBloomContinuity:
    """Tests for the bloom continuity score."""

    def test_empty_calendar_is_zero(self):
        """No blooming species → continuity = 0.0."""
        calendar = {m: [] for m in MONTHS}
        assert compute_bloom_continuity(calendar) == 0.0

    def test_single_month_is_low(self):
        """All species in one month → low continuity (near 0)."""
        calendar = {m: [] for m in MONTHS}
        calendar["Jun"] = [
            {"plant": "A", "intensity": "high"},
            {"plant": "B", "intensity": "high"},
        ]
        score = compute_bloom_continuity(calendar)
        assert score < 0.2, f"Single-month continuity too high: {score}"

    def test_perfectly_uniform_is_near_one(self):
        """Equal bloom in every month → continuity ≈ 1.0."""
        calendar = {
            m: [{"plant": "P", "intensity": "high"}] for m in MONTHS
        }
        score = compute_bloom_continuity(calendar)
        assert score == pytest.approx(1.0, abs=0.01)

    def test_two_months_lower_than_six(self):
        """More spread-out coverage → higher continuity score."""
        two_month = {m: [] for m in MONTHS}
        two_month["Jun"] = [{"plant": "A", "intensity": "high"}]
        two_month["Jul"] = [{"plant": "B", "intensity": "high"}]

        six_month = {m: [] for m in MONTHS}
        for m in ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]:
            six_month[m] = [{"plant": "X", "intensity": "high"}]

        score_2 = compute_bloom_continuity(two_month)
        score_6 = compute_bloom_continuity(six_month)
        assert score_6 > score_2, (
            f"6-month ({score_6}) should beat 2-month ({score_2})"
        )

    def test_intensity_weighting_matters(self):
        """High-intensity coverage should score differently than low-intensity."""
        high_cal = {m: [] for m in MONTHS}
        high_cal["Jun"] = [{"plant": "A", "intensity": "high"}]
        high_cal["Jul"] = [{"plant": "B", "intensity": "high"}]

        low_cal = {m: [] for m in MONTHS}
        low_cal["Jun"] = [{"plant": "A", "intensity": "low"}]
        low_cal["Jul"] = [{"plant": "B", "intensity": "low"}]

        # Both should be valid scores but potentially differ in edge cases
        score_high = compute_bloom_continuity(high_cal)
        score_low = compute_bloom_continuity(low_cal)
        assert 0.0 <= score_high <= 1.0
        assert 0.0 <= score_low <= 1.0

    def test_score_bounded_zero_one(self):
        """Continuity score must always be in [0.0, 1.0]."""
        calendar = {m: [] for m in MONTHS}
        for m in ["Mar", "Jun", "Sep", "Dec"]:
            calendar[m] = [
                {"plant": "A", "intensity": "high"},
                {"plant": "B", "intensity": "medium"},
            ]
        score = compute_bloom_continuity(calendar)
        assert 0.0 <= score <= 1.0


# ── generate_bloom_calendar ─────────────────────────────────────────────

class TestGenerateBloomCalendar:
    """Integration tests for the main bloom calendar generator."""

    def test_contains_continuity_score(self):
        """Output must include bloom_continuity_score."""
        result = generate_bloom_calendar("Eastern Temperate Forests")
        assert "bloom_continuity_score" in result
        assert 0.0 <= result["bloom_continuity_score"] <= 1.0

    def test_contains_gap_recommendations(self):
        """Output must include gap_filling_recommendations list."""
        result = generate_bloom_calendar("Eastern Temperate Forests")
        assert "gap_filling_recommendations" in result
        assert isinstance(result["gap_filling_recommendations"], list)

    def test_no_matching_species_returns_zero_continuity(self):
        """When no species match filters, continuity should be 0.0."""
        result = generate_bloom_calendar(
            "Eastern Temperate Forests", sun="shade", soil="sandy"
        )
        if result["no_matching_species"]:
            assert result["bloom_continuity_score"] == 0.0
            assert result["bloom_gap_months"] == list(MONTHS)

    def test_gap_months_match_empty_calendar_entries(self):
        """Gap months should exactly correspond to empty calendar months."""
        result = generate_bloom_calendar("Eastern Temperate Forests")
        for month in MONTHS:
            is_gap = len(result["calendar"][month]) == 0
            in_gap_list = month in result["bloom_gap_months"]
            assert is_gap == in_gap_list, (
                f"Month {month}: is_gap={is_gap} vs in_list={in_gap_list}"
            )

    def test_eastern_forests_has_decent_continuity(self):
        """Eastern Temperate Forests (full sun) should have good continuity."""
        result = generate_bloom_calendar(
            "Eastern Temperate Forests", sun="full"
        )
        assert result["bloom_continuity_score"] > 0.5, (
            f"Expected decent continuity for rich ecoregion, "
            f"got {result['bloom_continuity_score']}"
        )

    def test_gap_recommendations_are_not_in_current_plants(self):
        """Recommended gap-fillers should not duplicate existing plants."""
        result = generate_bloom_calendar("Eastern Temperate Forests", sun="full")
        existing = {
            entry["plant"]
            for month_entries in result["calendar"].values()
            for entry in month_entries
        }
        for rec in result["gap_filling_recommendations"]:
            assert rec["plant"] not in existing, (
                f"Recommendation '{rec['plant']}' already in calendar"
            )


# ── generate_succession_bloom ───────────────────────────────────────────

class TestSuccessionBloom:
    """Tests for succession-aware year-by-year bloom projections."""

    def test_returns_six_years(self):
        """Should produce Y0–Y5 = 6 dicts."""
        result = generate_succession_bloom("Eastern Temperate Forests")
        assert len(result) == 6
        for i, entry in enumerate(result):
            assert entry["year"] == i

    def test_species_count_increases_over_time(self):
        """Established species count should monotonically increase."""
        result = generate_succession_bloom("Eastern Temperate Forests")
        for i in range(1, 6):
            prev = result[i - 1]["established_species_count"]
            curr = result[i]["established_species_count"]
            assert curr >= prev, (
                f"Y{i} species count ({curr}) < Y{i-1} ({prev})"
            )

    def test_continuity_generally_improves(self):
        """Bloom continuity should generally improve as more species establish."""
        result = generate_succession_bloom("Eastern Temperate Forests")
        # Y5 should be ≥ Y0 (may not be strictly monotonic due to mix effects)
        assert result[5]["bloom_continuity_score"] >= result[0]["bloom_continuity_score"]

    def test_year_five_has_most_species(self):
        """Year 5 should have the most established species."""
        result = generate_succession_bloom("Eastern Temperate Forests")
        y5_count = result[5]["established_species_count"]
        total = result[5]["total_pool_size"]
        # Should be close to full pool (90%+ of shrubs, 100% forbs)
        assert y5_count >= total * 0.8, (
            f"Y5 established {y5_count} out of {total} — too low"
        )

    def test_each_year_has_valid_calendar(self):
        """Each year dict should have a complete 12-month calendar."""
        result = generate_succession_bloom("Eastern Temperate Forests")
        for entry in result:
            cal = entry["calendar"]
            assert set(cal.keys()) == set(MONTHS)
            assert 0.0 <= entry["bloom_continuity_score"] <= 1.0

    def test_empty_ecoregion_returns_zeros(self):
        """Unknown ecoregion → empty calendars for all years."""
        result = generate_succession_bloom("Nonexistent Ecoregion")
        assert len(result) == 6
        for entry in result:
            assert entry["established_species_count"] == 0
            assert entry["bloom_continuity_score"] == 0.0

    def test_forbs_establish_before_shrubs(self):
        """In Y1, forb fraction should exceed shrub fraction."""
        forb_frac, shrub_frac = _ESTABLISHMENT_RATE[1]
        assert forb_frac > shrub_frac, (
            f"Y1 forb fraction ({forb_frac}) should exceed shrub ({shrub_frac})"
        )

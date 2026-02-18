"""Unit tests for interactions.py Shannon-Wiener diversity enhancement.

Covers:
- Shannon-Wiener index (compute_shannon_wiener)
- Pielou's evenness (compute_evenness)
- Integration with build_food_web stats
- Edge cases: empty, single species, perfectly even
"""

import math
import pytest
from app.engine.interactions import (
    compute_shannon_wiener,
    compute_evenness,
    build_food_web,
)


# ── compute_shannon_wiener ──────────────────────────────────────────────

class TestShannonWiener:
    """Tests for the Shannon-Wiener diversity index."""

    def test_empty_returns_zero(self):
        assert compute_shannon_wiener([]) == 0.0

    def test_single_species_returns_zero(self):
        """One species → H' = 0 (no diversity)."""
        assert compute_shannon_wiener([10]) == 0.0

    def test_two_equal_species(self):
        """Two equally abundant species → H' = ln(2) ≈ 0.693."""
        result = compute_shannon_wiener([50, 50])
        assert result == pytest.approx(math.log(2), abs=0.001)

    def test_three_equal_species(self):
        """Three equal → H' = ln(3) ≈ 1.099."""
        result = compute_shannon_wiener([100, 100, 100])
        assert result == pytest.approx(math.log(3), abs=0.001)

    def test_unequal_is_lower_than_equal(self):
        """Uneven distribution → lower H' than even."""
        even = compute_shannon_wiener([50, 50, 50, 50])
        uneven = compute_shannon_wiener([180, 10, 5, 5])
        assert even > uneven

    def test_all_zeros_returns_zero(self):
        assert compute_shannon_wiener([0, 0, 0]) == 0.0

    def test_result_always_non_negative(self):
        """H' should never be negative."""
        cases = [[1], [1, 1], [100, 1], [0, 0], [1, 2, 3, 4, 5]]
        for c in cases:
            assert compute_shannon_wiener(c) >= 0.0

    def test_more_species_higher_diversity(self):
        """Equal-abundance communities: more species → higher H'."""
        h2 = compute_shannon_wiener([10, 10])
        h5 = compute_shannon_wiener([10, 10, 10, 10, 10])
        h10 = compute_shannon_wiener([10] * 10)
        assert h5 > h2
        assert h10 > h5


# ── compute_evenness ────────────────────────────────────────────────────

class TestEvenness:
    """Tests for Pielou's evenness index J'."""

    def test_single_species_zero(self):
        assert compute_evenness(0.0, 1) == 0.0

    def test_perfectly_even_is_one(self):
        """When H' = ln(S), evenness = 1.0."""
        s = 5
        h = math.log(s)
        assert compute_evenness(h, s) == pytest.approx(1.0, abs=0.001)

    def test_bounded_zero_one(self):
        """Evenness should always be in [0, 1]."""
        h = compute_shannon_wiener([100, 1, 1, 1])
        j = compute_evenness(h, 4)
        assert 0.0 <= j <= 1.0

    def test_uneven_lower_than_even(self):
        """Uneven distribution → lower J' than even."""
        h_even = compute_shannon_wiener([50, 50, 50])
        h_uneven = compute_shannon_wiener([90, 5, 5])
        j_even = compute_evenness(h_even, 3)
        j_uneven = compute_evenness(h_uneven, 3)
        assert j_even > j_uneven


# ── build_food_web integration ──────────────────────────────────────────

class TestFoodWebDiversityStats:
    """Integration tests: Shannon-Wiener index in food web stats."""

    def test_stats_include_diversity_fields(self):
        """Food web stats should include shannon_wiener_index and evenness."""
        web = build_food_web(
            ecoregion="Eastern Temperate Forests",
            interventions=["native_meadow"],
            sun="full",
        )
        for year in range(6):
            stats = web[year]["stats"]
            assert "shannon_wiener_index" in stats
            assert "evenness" in stats
            assert stats["shannon_wiener_index"] >= 0.0
            assert 0.0 <= stats["evenness"] <= 1.0

    def test_diversity_generally_increases(self):
        """Diversity should trend upward as the food web develops."""
        web = build_food_web(
            ecoregion="Eastern Temperate Forests",
            interventions=["native_meadow"],
            sun="full",
        )
        h_y0 = web[0]["stats"]["shannon_wiener_index"]
        h_y5 = web[5]["stats"]["shannon_wiener_index"]
        assert h_y5 >= h_y0, (
            f"Y5 H' ({h_y5}) should be >= Y0 H' ({h_y0})"
        )

    def test_connectance_uses_directed_formula(self):
        """Connectance should be based on n*(n-1) not n*(n-1)/2."""
        web = build_food_web(
            ecoregion="Eastern Temperate Forests",
            interventions=["native_meadow"],
            sun="full",
        )
        for year in range(6):
            stats = web[year]["stats"]
            n = stats["total_nodes"]
            e = stats["total_edges"]
            if n > 1:
                max_dir = n * (n - 1)
                expected = round(e / max_dir, 3)
                assert stats["connectance"] == expected, (
                    f"Y{year}: connectance mismatch "
                    f"(got {stats['connectance']}, expected {expected})"
                )

    def test_empty_web_has_zero_diversity(self):
        """No matching species → H' = 0, evenness = 0."""
        web = build_food_web(
            ecoregion="Great Plains",
            interventions=["native_meadow"],
            sun="shade",
            soil="well_drained",
        )
        stats = web[0]["stats"]
        assert stats["shannon_wiener_index"] == 0.0
        assert stats["evenness"] == 0.0

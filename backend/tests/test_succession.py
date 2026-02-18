"""Unit tests for succession.py enhancements.

Covers:
- Logistic scaling function (_logistic_scale)
- Clamping function (_clamp)
- Per-metric weight differentiation
- Soil-type cross-effects
- Multi-intervention synergy (compute_synergy)
- Full trajectory (simulate_trajectory) boundary & regression checks
"""

import pytest
from app.engine.succession import (
    _logistic_scale,
    _clamp,
    compute_synergy,
    simulate_trajectory,
    _SYNERGY,
    _SOIL_MOD,
    _BASE,
    _METRICS,
    POLLINATOR,
    BIRD,
    FOOD_WEB,
    SERVICES,
)


# ── Helpers ──────────────────────────────────────────────────────────────

_ALL_METRICS = [
    "pollinator_diversity_index",
    "bird_activity_score",
    "food_web_complexity",
    "ecosystem_services_score",
]


def _y3(traj: dict) -> dict:
    """Convenience: return the Year 3 dict from a trajectory."""
    return traj["years"][3]


# ── _clamp ───────────────────────────────────────────────────────────────

class TestClamp:
    """Tests for the _clamp utility."""

    def test_clamp_within_range_unchanged(self):
        assert _clamp(0.5) == 0.5

    def test_clamp_negative_to_zero(self):
        assert _clamp(-0.1) == 0.0

    def test_clamp_above_one_to_one(self):
        assert _clamp(1.5) == 1.0

    def test_clamp_rounds_to_three_decimals(self):
        assert _clamp(0.12345) == 0.123

    def test_clamp_boundary_zero(self):
        assert _clamp(0.0) == 0.0

    def test_clamp_boundary_one(self):
        assert _clamp(1.0) == 1.0


# ── _logistic_scale ──────────────────────────────────────────────────────

class TestLogisticScale:
    """Tests for the logistic scaling function."""

    def test_neutral_modifier_returns_base(self):
        """mod=1.0 should leave the base value unchanged."""
        assert _logistic_scale(0.5, 1.0) == pytest.approx(0.5, abs=1e-9)

    def test_zero_base_stays_zero(self):
        """v=0 → result=0 regardless of modifier."""
        assert _logistic_scale(0.0, 1.5) == pytest.approx(0.0, abs=1e-9)

    def test_boost_modifier_increases_value(self):
        """mod>1 should increase the output above the base."""
        result = _logistic_scale(0.5, 1.3)
        assert result > 0.5

    def test_penalty_modifier_decreases_value(self):
        """mod<1 should decrease the output below the base."""
        result = _logistic_scale(0.5, 0.7)
        assert result < 0.5

    def test_high_base_high_mod_no_overflow(self):
        """The key regression: 0.75 * 1.25 = 0.9375 linearly → logistic < 0.9375."""
        result = _logistic_scale(0.75, 1.25)
        assert result < 0.75 * 1.25, "Logistic should compress, not exceed linear"
        assert result > 0.75, "Boost modifier should still increase"

    def test_stacked_modifiers_no_saturation(self):
        """Stacked mods like 1.25 * 1.3 should not hit 1.0."""
        result = _logistic_scale(0.58, 1.625)
        assert result < 1.0, "Should not saturate to 1.0"
        assert result > 0.58, "Should be higher than base"

    def test_low_base_behaves_nearly_linearly(self):
        """For small base values, logistic ≈ linear (both regimes agree)."""
        base = 0.05
        mod = 1.2
        logistic = _logistic_scale(base, mod)
        linear = base * mod
        assert abs(logistic - linear) < 0.01, "Should be nearly linear for small base"

    def test_diminishing_returns(self):
        """Bigger boosts yield smaller marginal gains at high base values."""
        gain_small = _logistic_scale(0.8, 1.1) - 0.8
        gain_big = _logistic_scale(0.8, 1.2) - 0.8
        ratio = gain_big / gain_small
        # Linear would give ratio=2.0; logistic should be < 2.0
        assert ratio < 2.0, "Should exhibit diminishing returns"

    def test_result_always_non_negative(self):
        """Output should never go negative."""
        cases = [(0.0, 0.0), (0.01, 0.01), (0.5, 0.5), (1.0, 1.0)]
        for base, mod in cases:
            assert _logistic_scale(base, mod) >= 0.0


# ── compute_synergy ─────────────────────────────────────────────────────

class TestComputeSynergy:
    """Tests for multi-intervention synergy calculation."""

    def test_single_intervention_neutral(self):
        """One intervention → no pairs → all 1.0."""
        result = compute_synergy(["native_meadow"])
        assert result == (1.0, 1.0, 1.0, 1.0)

    def test_empty_list_neutral(self):
        """Empty list → no pairs → all 1.0."""
        result = compute_synergy([])
        assert result == (1.0, 1.0, 1.0, 1.0)

    def test_known_pair_returns_expected(self):
        """A known pair should return its synergy coefficients."""
        result = compute_synergy(["native_meadow", "pollinator_nesting"])
        expected = _SYNERGY[frozenset({"native_meadow", "pollinator_nesting"})]
        assert result == expected

    def test_pair_order_independent(self):
        """Synergy should not depend on the order of interventions."""
        r1 = compute_synergy(["native_meadow", "pollinator_nesting"])
        r2 = compute_synergy(["pollinator_nesting", "native_meadow"])
        assert r1 == r2

    def test_unknown_pair_neutral(self):
        """Interventions with no synergy entry → neutral (1.0)."""
        result = compute_synergy(["stop_mowing", "native_grass"])
        assert result == (1.0, 1.0, 1.0, 1.0)

    def test_triple_multiplies_all_pairs(self):
        """Three interventions → three pairs → coefficients multiply."""
        interventions = ["native_meadow", "pollinator_nesting", "habitat_structures"]
        result = compute_synergy(interventions)

        # Manual multiplication of the three pairs
        p1 = _SYNERGY[frozenset({"native_meadow", "pollinator_nesting"})]
        p2 = _SYNERGY[frozenset({"native_meadow", "habitat_structures"})]
        p3 = _SYNERGY[frozenset({"pollinator_nesting", "habitat_structures"})]

        for k in range(4):
            expected = p1[k] * p2[k] * p3[k]
            assert result[k] == pytest.approx(expected, abs=1e-9)

    def test_all_synergy_coefficients_positive(self):
        """Every synergy coefficient in the table should be > 0."""
        for pair, coeffs in _SYNERGY.items():
            for c in coeffs:
                assert c > 0, f"Non-positive synergy in {pair}: {coeffs}"

    def test_synergy_always_above_one(self):
        """All synergy coefficients should be ≥ 1.0 (no negative synergy)."""
        for pair, coeffs in _SYNERGY.items():
            for c in coeffs:
                assert c >= 1.0, f"Synergy < 1.0 in {pair}: {coeffs}"


# ── Soil type cross-effects ─────────────────────────────────────────────

class TestSoilEffects:
    """Tests for soil-type cross-effect modifiers."""

    def test_unknown_soil_is_neutral(self):
        """Unknown soil should have all-1.0 modifiers for every intervention."""
        for intervention, mods in _SOIL_MOD["unknown"].items():
            assert mods == (1.0, 1.0, 1.0, 1.0), f"unknown/{intervention} != neutral"

    def test_clay_boosts_rain_garden(self):
        """Rain gardens on clay should score higher than on well-drained."""
        clay_traj = simulate_trajectory(
            "75254", "rain_garden", 500, "maintained_lawn", "full", "clay"
        )
        wd_traj = simulate_trajectory(
            "75254", "rain_garden", 500, "maintained_lawn", "full", "well_drained"
        )
        clay_svc = _y3(clay_traj)["ecosystem_services_score"]
        wd_svc = _y3(wd_traj)["ecosystem_services_score"]
        assert clay_svc > wd_svc, (
            f"Clay rain garden services ({clay_svc}) should exceed "
            f"well-drained ({wd_svc})"
        )

    def test_clay_penalizes_meadow(self):
        """Native meadow on clay should score lower than on well-drained."""
        clay_traj = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full", "clay"
        )
        wd_traj = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full", "well_drained"
        )
        clay_poll = _y3(clay_traj)["pollinator_diversity_index"]
        wd_poll = _y3(wd_traj)["pollinator_diversity_index"]
        assert clay_poll < wd_poll, (
            f"Clay meadow pollinators ({clay_poll}) should be below "
            f"well-drained ({wd_poll})"
        )

    def test_soil_differentiates_metrics(self):
        """Sandy soil should penalize services more than pollinators for meadow."""
        sandy = _SOIL_MOD["sandy"]["native_meadow"]
        assert sandy[SERVICES] < sandy[POLLINATOR], (
            "Sandy meadow services penalty should be larger than pollinator penalty"
        )


# ── Per-metric weights ──────────────────────────────────────────────────

class TestPerMetricWeights:
    """Tests for per-metric area/sun/soil weighting."""

    def test_shade_hurts_pollinators_more_than_birds(self):
        """Sun weight is 1.3 for pollinators vs 0.8 for birds → bigger drop."""
        full = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full", "well_drained"
        )
        shade = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "shade", "well_drained"
        )
        poll_drop = _y3(full)["pollinator_diversity_index"] - _y3(shade)["pollinator_diversity_index"]
        bird_drop = _y3(full)["bird_activity_score"] - _y3(shade)["bird_activity_score"]
        assert poll_drop > bird_drop, (
            f"Pollinator drop ({poll_drop:.4f}) should exceed bird drop ({bird_drop:.4f})"
        )

    def test_large_area_helps_birds_more_than_pollinators(self):
        """Area weight is 1.4 for birds vs 0.8 for pollinators → bigger gain."""
        small = simulate_trajectory(
            "75254", "native_meadow", 200, "maintained_lawn", "full", "well_drained"
        )
        large = simulate_trajectory(
            "75254", "native_meadow", 10000, "maintained_lawn", "full", "well_drained"
        )
        poll_gain = _y3(large)["pollinator_diversity_index"] - _y3(small)["pollinator_diversity_index"]
        bird_gain = _y3(large)["bird_activity_score"] - _y3(small)["bird_activity_score"]
        assert bird_gain > poll_gain, (
            f"Bird gain ({bird_gain:.4f}) should exceed pollinator gain ({poll_gain:.4f})"
        )


# ── simulate_trajectory boundary & regression ───────────────────────────

class TestSimulateTrajectory:
    """Boundary checks and regression tests for the full trajectory."""

    def test_all_values_bounded_zero_one(self):
        """Every metric in every year should be in [0.0, 1.0]."""
        traj = simulate_trajectory(
            "33139", "native_meadow", 500, "partial_garden", "full", "well_drained"
        )
        for y_data in traj["years"]:
            for m in _ALL_METRICS:
                assert 0.0 <= y_data[m] <= 1.0, (
                    f"Y{y_data['year']} {m}={y_data[m]} out of bounds"
                )

    def test_trajectory_monotonically_increasing(self):
        """Metrics should generally increase year-over-year for standard scenario."""
        traj = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full", "well_drained"
        )
        for m in _ALL_METRICS:
            for i in range(1, 6):
                prev = traj["years"][i - 1][m]
                curr = traj["years"][i][m]
                assert curr >= prev, (
                    f"{m} decreased from Y{i-1} ({prev}) to Y{i} ({curr})"
                )

    def test_year_zero_is_near_zero(self):
        """Year 0 represents pre-intervention baseline → low values."""
        traj = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full", "well_drained"
        )
        y0 = traj["years"][0]
        for m in _ALL_METRICS:
            assert y0[m] < 0.15, f"Y0 {m}={y0[m]} should be near-zero baseline"

    def test_high_mod_scenario_no_saturation(self):
        """partial_garden + Florida + full sun should NOT produce 1.0 in any metric."""
        traj = simulate_trajectory(
            "33139", "native_meadow", 5000, "partial_garden", "full", "well_drained"
        )
        y5 = traj["years"][5]
        for m in _ALL_METRICS:
            assert y5[m] < 1.0, (
                f"Saturated! Y5 {m}={y5[m]} hit ceiling despite logistic curve"
            )

    def test_synergy_boosts_trajectory(self):
        """Passing synergy > 1.0 should produce higher scores than neutral."""
        syn = compute_synergy(["native_meadow", "pollinator_nesting"])
        with_syn = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full",
            "well_drained", synergy=syn,
        )
        without_syn = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full",
            "well_drained",
        )
        y3_syn = _y3(with_syn)["pollinator_diversity_index"]
        y3_base = _y3(without_syn)["pollinator_diversity_index"]
        assert y3_syn > y3_base, (
            f"Synergy pollinator ({y3_syn}) should exceed baseline ({y3_base})"
        )

    def test_all_interventions_produce_trajectories(self):
        """Every intervention in _BASE should produce a valid 6-year trajectory."""
        for intervention in _BASE:
            traj = simulate_trajectory(
                "75254", intervention, 500, "maintained_lawn", "full", "well_drained"
            )
            assert len(traj["years"]) == 6, f"{intervention}: expected 6 years"
            for y_data in traj["years"]:
                for m in _ALL_METRICS:
                    assert 0.0 <= y_data[m] <= 1.0, (
                        f"{intervention} Y{y_data['year']} {m}={y_data[m]} OOB"
                    )

    def test_unknown_intervention_falls_back_to_meadow(self):
        """Unknown intervention should fallback to native_meadow base."""
        traj = simulate_trajectory(
            "75254", "does_not_exist", 500, "maintained_lawn", "full", "well_drained"
        )
        meadow = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full", "well_drained"
        )
        # Should produce identical trajectories (same base data)
        for i in range(6):
            for m in _ALL_METRICS:
                assert traj["years"][i][m] == meadow["years"][i][m]

    def test_returns_correct_metadata(self):
        """Trajectory dict should include zone, ecoregion, and zip."""
        traj = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full", "well_drained"
        )
        assert traj["zip_code"] == "75254"
        assert traj["intervention"] == "native_meadow"
        assert "zone" in traj
        assert "ecoregion" in traj

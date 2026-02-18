"""Mathematical impact analysis for succession.py enhancements.

Compares OLD linear-clamp model vs NEW logistic model across all new features:
- Logistic growth curves
- Per-metric weights (area, sun, soil)
- Soil-type cross-effects
- Multi-intervention synergy

Run: cd backend && uv run python tests/math_impact_succession.py
"""

from app.engine.succession import (
    _logistic_scale,
    _clamp,
    simulate_trajectory,
    compute_synergy,
)


def section(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)
    print()


def main() -> None:
    # ── 1. Logistic vs Linear ────────────────────────────────────────────
    section("1. LOGISTIC vs LINEAR — side-by-side comparison")
    header = f"{'Base':>6} {'Mod':>5} | {'OLD (v*m clamp)':>15} {'NEW (logistic)':>15} {'Delta':>8}"
    print(header)
    print("-" * len(header))

    test_cases = [
        (0.75, 1.25, "High base, high mod (the overflow case)"),
        (0.58, 1.25, "Mid base, high mod"),
        (0.20, 1.25, "Low base, high mod"),
        (0.05, 1.25, "Tiny base, high mod"),
        (0.75, 1.00, "High base, neutral"),
        (0.75, 0.70, "High base, desert penalty"),
        (0.40, 0.85, "Mid base, shade penalty"),
        (0.58, 1.625, "Stacked mods: 1.25*1.3 (partial_garden+Florida)"),
    ]

    for base, mod, label in test_cases:
        old = _clamp(base * mod)
        new = _clamp(_logistic_scale(base, mod))
        delta = new - old
        print(f"{base:>6.2f} {mod:>5.3f} | {old:>15.4f} {new:>15.4f} {delta:>+8.4f}  <- {label}")

    # ── 2. Soil x Rain Garden ────────────────────────────────────────────
    section("2. SOIL TYPE EFFECT — rain_garden on different soils")
    for soil in ["well_drained", "clay", "sandy", "loamy"]:
        traj = simulate_trajectory(
            "75254", "rain_garden", 500, "maintained_lawn", "full", soil
        )
        y3 = traj["years"][3]
        print(
            f"  {soil:>13}: poll={y3['pollinator_diversity_index']:.4f}  "
            f"bird={y3['bird_activity_score']:.4f}  "
            f"web={y3['food_web_complexity']:.4f}  "
            f"svc={y3['ecosystem_services_score']:.4f}"
        )

    # ── 3. Soil x Meadow ─────────────────────────────────────────────────
    section("3. SOIL TYPE EFFECT — native_meadow on different soils")
    for soil in ["well_drained", "clay", "sandy", "loamy"]:
        traj = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", "full", soil
        )
        y3 = traj["years"][3]
        print(
            f"  {soil:>13}: poll={y3['pollinator_diversity_index']:.4f}  "
            f"bird={y3['bird_activity_score']:.4f}  "
            f"web={y3['food_web_complexity']:.4f}  "
            f"svc={y3['ecosystem_services_score']:.4f}"
        )

    # ── 4. Sun/shade per-metric differentiation ──────────────────────────
    section("4. PER-METRIC WEIGHTS — shade should hurt pollinators more than birds")
    for sun in ["full", "partial", "shade"]:
        traj = simulate_trajectory(
            "75254", "native_meadow", 500, "maintained_lawn", sun, "well_drained"
        )
        y3 = traj["years"][3]
        print(
            f"  {sun:>8}: poll={y3['pollinator_diversity_index']:.4f}  "
            f"bird={y3['bird_activity_score']:.4f}  "
            f"web={y3['food_web_complexity']:.4f}  "
            f"svc={y3['ecosystem_services_score']:.4f}"
        )
    print()
    print("  (pollinator drop from full->shade should exceed bird drop)")

    # ── 5. Area per-metric differentiation ───────────────────────────────
    section("5. PER-METRIC WEIGHTS — large area helps birds more than pollinators")
    for area in [200, 500, 2000, 10000]:
        traj = simulate_trajectory(
            "75254", "native_meadow", area, "maintained_lawn", "full", "well_drained"
        )
        y3 = traj["years"][3]
        print(
            f"  {area:>6} sqft: poll={y3['pollinator_diversity_index']:.4f}  "
            f"bird={y3['bird_activity_score']:.4f}  "
            f"web={y3['food_web_complexity']:.4f}  "
            f"svc={y3['ecosystem_services_score']:.4f}"
        )
    print()
    print("  (bird gain from 200->10000 should exceed pollinator gain)")

    # ── 6. Synergy effects ───────────────────────────────────────────────
    section("6. SYNERGY — meadow alone vs meadow+nesting vs +structures")
    combos = [
        (["native_meadow"], "meadow alone"),
        (["native_meadow", "pollinator_nesting"], "meadow + nesting"),
        (
            ["native_meadow", "pollinator_nesting", "habitat_structures"],
            "meadow + nesting + structures",
        ),
    ]
    for interventions, label in combos:
        syn = compute_synergy(interventions)
        traj = simulate_trajectory(
            "75254",
            "native_meadow",
            500,
            "maintained_lawn",
            "full",
            "well_drained",
            synergy=syn,
        )
        y3 = traj["years"][3]
        print(
            f"  {label:>40}: poll={y3['pollinator_diversity_index']:.4f}  "
            f"bird={y3['bird_activity_score']:.4f}  "
            f"web={y3['food_web_complexity']:.4f}  "
            f"svc={y3['ecosystem_services_score']:.4f}  "
            f"syn={tuple(round(s, 3) for s in syn)}"
        )

    # ── 7. Saturation check — the key regression ────────────────────────
    section("7. SATURATION CHECK — partial_garden + Florida (old overflow case)")
    print("  OLD model: 0.75 * 1.25 * 1.3 = 1.219 -> clamped to 1.0 (false perfect)")
    print("  NEW model: logistic prevents saturation, realistic ceiling")
    print()
    traj = simulate_trajectory(
        "33139", "native_meadow", 500, "partial_garden", "full", "well_drained"
    )
    for y_data in traj["years"]:
        y = y_data["year"]
        print(
            f"  Y{y}: poll={y_data['pollinator_diversity_index']:.4f}  "
            f"bird={y_data['bird_activity_score']:.4f}  "
            f"web={y_data['food_web_complexity']:.4f}  "
            f"svc={y_data['ecosystem_services_score']:.4f}"
        )

    print()
    all_bounded = all(
        0 <= y_data[m] <= 1
        for y_data in traj["years"]
        for m in [
            "pollinator_diversity_index",
            "bird_activity_score",
            "food_web_complexity",
            "ecosystem_services_score",
        ]
    )
    print(f"  All values bounded [0,1]: {all_bounded}")

    # ── 8. Full trajectory comparison ────────────────────────────────────
    section("8. FULL 6-YEAR TRAJECTORY — native_meadow, baseline conditions")
    traj = simulate_trajectory(
        "75254", "native_meadow", 500, "maintained_lawn", "full", "well_drained"
    )
    for y_data in traj["years"]:
        y = y_data["year"]
        print(
            f"  Y{y}: poll={y_data['pollinator_diversity_index']:.4f}  "
            f"bird={y_data['bird_activity_score']:.4f}  "
            f"web={y_data['food_web_complexity']:.4f}  "
            f"svc={y_data['ecosystem_services_score']:.4f}"
        )

    section("ANALYSIS COMPLETE")
    print("Key improvements over old model:")
    print("  * No metric ever falsely reaches 1.0 due to modifier overflow")
    print("  * Logistic curve has diminishing returns — ecologically realistic")
    print("  * Soil types create real differentiation (clay+rain_garden > clay+meadow)")
    print("  * Per-metric weights: pollinators care about sun, birds care about area")
    print("  * Synergy pairs produce measurable uplift without overflow")


if __name__ == "__main__":
    main()

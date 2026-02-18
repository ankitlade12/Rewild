import unittest

from app.engine.bloom_calendar import generate_bloom_calendar
from app.engine.interactions import build_food_web


class EcologyOutputTests(unittest.TestCase):
    def test_bloom_calendar_flags_no_matching_species(self):
        bloom = generate_bloom_calendar(
            ecoregion="Great Plains",
            sun="shade",
            soil="well_drained",
        )

        self.assertEqual(bloom["total_species"], 0)
        self.assertTrue(bloom["no_matching_species"])
        # When no species match, every month is a gap
        self.assertEqual(len(bloom["bloom_gap_months"]), 12)

    def test_food_web_does_not_add_pollinators_without_supported_plants(self):
        web = build_food_web(
            ecoregion="Great Plains",
            interventions=["native_meadow"],
            sun="shade",
            soil="well_drained",
        )

        poll_counts = [web[year]["stats"]["pollinator_count"] for year in range(6)]
        node_counts = [web[year]["stats"]["total_nodes"] for year in range(6)]

        self.assertEqual(poll_counts, [0, 0, 0, 0, 0, 0])
        self.assertEqual(node_counts, [0, 0, 0, 0, 0, 0])

    def test_food_web_pollinator_counts_progress_in_supported_conditions(self):
        web = build_food_web(
            ecoregion="Great Plains",
            interventions=["native_meadow"],
            sun="full",
            soil="well_drained",
        )

        poll_counts = [web[year]["stats"]["pollinator_count"] for year in range(6)]

        self.assertGreater(poll_counts[-1], poll_counts[0])
        self.assertGreater(len(set(poll_counts)), 1)


if __name__ == "__main__":
    unittest.main()

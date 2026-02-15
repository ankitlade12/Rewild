import unittest

from app.data.native_plants import get_native_plants


class NativePlantsFilteringTests(unittest.TestCase):
    def test_shade_filter_returns_shade_plants(self):
        plants = get_native_plants("Pacific Northwest Forests", sun="shade")

        self.assertGreater(len(plants), 0)
        self.assertTrue(
            all(p["sun_requirement"].lower().startswith("full shade") for p in plants)
        )


if __name__ == "__main__":
    unittest.main()

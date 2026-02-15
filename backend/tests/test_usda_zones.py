import unittest

from app.data.usda_zones import ZIP_TO_STATE, ZIP_TO_ZONE


class USDAZoneMappingTests(unittest.TestCase):
    def test_all_known_zone_prefixes_have_state_mapping(self):
        missing = sorted(prefix for prefix in ZIP_TO_ZONE if prefix not in ZIP_TO_STATE)
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()

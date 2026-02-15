import unittest

from app.engine.action_plan import generate_action_plan


class ActionPlanFrostTests(unittest.TestCase):
    def test_frost_free_zone_does_not_include_last_frost_task(self):
        plan = generate_action_plan(
            zip_code="33101",
            intervention="native_meadow",
            area_sqft=500,
            sun="full",
            soil="well_drained",
        )

        tasks = [
            task["task"]
            for month_tasks in plan["planting_calendar"].values()
            for task in month_tasks
        ]

        self.assertTrue(plan["last_frost"].lower().startswith("frost-free"))
        self.assertFalse(any("last frost" in t.lower() for t in tasks))


if __name__ == "__main__":
    unittest.main()

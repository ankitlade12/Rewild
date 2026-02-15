import unittest
from unittest.mock import AsyncMock, patch

import httpx

from app.main import app


class APIRouteTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(transport=self.transport, base_url="http://testserver")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_health(self):
        resp = await self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("status"), "ok")

    async def test_lookup_success(self):
        resp = await self.client.get("/api/lookup/75254")
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["zip_code"], "75254")
        self.assertIn("zone", body)
        self.assertIn("ecoregion", body)
        self.assertIn("state", body)

    async def test_lookup_invalid_zip_format_returns_422(self):
        resp = await self.client.get("/api/lookup/75a54")
        self.assertEqual(resp.status_code, 422)

    async def test_lookup_unknown_zip_returns_404(self):
        resp = await self.client.get("/api/lookup/99999")
        self.assertEqual(resp.status_code, 404)

    async def test_simulate_success(self):
        payload = {
            "site_profile": {
                "zip_code": "75254",
                "area_sqft": 1000,
                "current_state": "maintained_lawn",
                "sun_exposure": "full",
                "soil_type": "well_drained",
                "goals": ["pollinators"],
            },
            "interventions": ["native_meadow", "rain_garden"],
        }

        mock_response = {
            "narrative": "Mocked narrative",
            "species_recommendations": [],
            "uncertainty_note": "Mocked",
            "season_tip": "Mocked",
            "source": "mock",
        }

        with patch("app.routes.simulate.get_narrative", new=AsyncMock(return_value=mock_response)) as mock_narrative:
            resp = await self.client.post("/api/simulate", json=payload)

        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["scenario_count"], 2)
        self.assertEqual(len(body["scenarios"]), 2)
        self.assertEqual(mock_narrative.await_count, 2)

        for scenario in body["scenarios"]:
            self.assertIn("timeline", scenario)
            self.assertEqual(len(scenario["timeline"]), 6)
            self.assertIn("narrative", scenario)
            self.assertEqual(scenario["narrative"]["source"], "mock")

    async def test_simulate_missing_site_profile_returns_422(self):
        payload = {"interventions": ["native_meadow"]}
        resp = await self.client.post("/api/simulate", json=payload)
        self.assertEqual(resp.status_code, 422)

    async def test_action_plan_success(self):
        payload = {
            "zip_code": "75254",
            "intervention": "native_meadow",
            "area_sqft": 1000,
            "sun": "full",
            "soil": "well_drained",
        }
        resp = await self.client.post("/api/action-plan", json=payload)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["intervention"], "native_meadow")
        self.assertIn("planting_calendar", body)
        self.assertIn("shopping_list", body)

    async def test_action_plan_missing_zip_returns_422(self):
        payload = {
            "intervention": "native_meadow",
            "area_sqft": 1000,
            "sun": "full",
            "soil": "well_drained",
        }
        resp = await self.client.post("/api/action-plan", json=payload)
        self.assertEqual(resp.status_code, 422)


if __name__ == "__main__":
    unittest.main()

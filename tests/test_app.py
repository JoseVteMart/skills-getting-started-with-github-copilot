import pytest

from httpx import AsyncClient

from src.app import app, activities


@pytest.mark.asyncio
async def test_get_activities():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/activities")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, dict)
        # sample activity present
        assert "Chess Club" in data


@pytest.mark.asyncio
async def test_signup_duplicate_and_unregister():
    activity = "Basketball Team"
    email = "testuser@example.com"

    # ensure clean state for this activity
    activities.setdefault(activity, {"participants": []})
    activities[activity]["participants"] = []

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Signup should succeed
        r = await ac.post(f"/activities/{activity}/signup?email={email}")
        assert r.status_code == 200
        assert email in activities[activity]["participants"]

        # Duplicate signup should fail (400)
        r_dup = await ac.post(f"/activities/{activity}/signup?email={email}")
        assert r_dup.status_code == 400

        # Unregister should succeed
        r_un = await ac.post(f"/activities/{activity}/unregister?email={email}")
        assert r_un.status_code == 200
        assert email not in activities[activity]["participants"]

        # Unregistering again should fail (400)
        r_un2 = await ac.post(f"/activities/{activity}/unregister?email={email}")
        assert r_un2.status_code == 400

"""
Test the golden path of user authentication, movie creation, review submission,
and fetching movie details including reviews.
This end-to-end test ensures that all components work together as expected.
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
# from asgi_lifespan import LifespanManager

from app.main import app


@pytest.fixture
# @pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

# @pytest_asyncio.fixture
# async def async_client():
#     async with LifespanManager(app):  # 🔥 runs startup/shutdown
#         transport = ASGITransport(app=app)
#         async with AsyncClient(
#             transport=transport,
#             base_url="http://test",
#         ) as client:
#             yield client

# 📝update the test so it explicitly uses the clean_db fixture,
# instead of relying on autouse=True in conftest.py
@pytest.mark.asyncio
async def test_auth_movie_review_vertical_slice(
    async_client: AsyncClient,  # your existing HTTP client
    clean_db  # <-- explicitly include the fixture here
):
    """
    Golden path:
    user → auth → movie → review → movie detail
    """
    # --- 1. Register user ---
    register_resp = await async_client.post(
        "/auth/register",
        json={
            "email": "golden@example.com",
            "password": "strongpassword",
        },
    )
    assert register_resp.status_code == 201

    # --- 2. Login ---
    login_resp = await async_client.post(
        "/auth/login",
        data={
            "username": "golden@example.com",
            "password": "strongpassword",
        },
    )
    assert login_resp.status_code == 200

    tokens = login_resp.json()
    access_token = tokens["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    # --- 3. Create movie ---
    movie_resp = await async_client.post(
        "/movies",
        json={
            "title": "Creed I",
            "release_year": 2015,
            "runtime": 133,
            "rating": 7.6,
            "genres": ["Drama", "Action"]
        },
        headers=headers,
    )
    assert movie_resp.status_code == 201

    movie = movie_resp.json()
    movie_id = movie["id"]

    # --- 4. Create review ---
    review_resp = await async_client.post(
        f"/reviews/movies/{movie_id}",
        json={"content": "Fantastic movie"},
        headers=headers,
    )
    assert review_resp.status_code == 201

    # --- 5. Fetch movie detail ---
    detail_resp = await async_client.get(
        f"/movies/{movie_id}",
        headers=headers,
    )
    assert detail_resp.status_code == 200

    detail = detail_resp.json()

    # --- 6. Assert review present ---
    assert len(detail["reviews"]) == 1
    assert detail["reviews"][0]["content"] == "Fantastic movie"

    # --- 7. Duplicate review should fail ---
    dup_resp = await async_client.post(
        f"/reviews/movies/{movie_id}",
        json={"content": "Second review"},
        headers=headers,
    )
    assert dup_resp.status_code == 400
    assert "already reviewed" in dup_resp.json()["detail"]

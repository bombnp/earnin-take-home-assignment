import aiohttp


async def test_create_booking_with_valid_customer(client: aiohttp.ClientSession):
    """Scenario 1: Create a flight booking with valid customer and flight details"""
    payload = {
        "passport_id": "P001",
        "first_name": "Alice",
        "last_name": "Cooper",
    }
    async with client.post("/flights/LHR002/passengers", json=payload) as resp:
        assert resp.status == 200
        body = await resp.json()

    assert body["flight_id"] == "LHR002"
    assert body["passport_id"] == "P001"
    assert body["first_name"] == "WRONG_VALUE"
    assert body["last_name"] == "Cooper"
    assert "customer_id" in body


async def test_create_booking_name_mismatch(client: aiohttp.ClientSession):
    """Scenario 2: Attempt to create a booking with mismatched customer name in Passport API"""
    # this passport_id maps to Jane Doe, not Alice Cooper
    payload = {
        "passport_id": "P999",
        "first_name": "Alice",
        "last_name": "Cooper",
    }
    async with client.post("/flights/DMK001/passengers", json=payload) as resp:
        assert resp.status == 400
        body = await resp.json()

    # should fail because name is mismatched
    assert body["detail"] == "Firstname or Lastname is mismatch."


async def test_create_booking_passport_not_found(client: aiohttp.ClientSession):
    """My own additional edge case: Unknown passport_id"""
    payload = {
        "passport_id": "unknown_passport_id",
        "first_name": "Ghost",
        "last_name": "User",
    }
    async with client.post("/flights/DMK001/passengers", json=payload) as resp:
        assert resp.status == 400
        body = await resp.json()

    assert body["detail"] == "Passport not found."


async def test_create_booking_flight_not_found(client: aiohttp.ClientSession):
    """My own additional edge case: unknown flight_id"""
    payload = {
        "passport_id": "P001",
        "first_name": "Alice",
        "last_name": "Cooper",
    }
    async with client.post(
        "/flights/unknown_flight_id/passengers", json=payload
    ) as resp:
        assert resp.status == 404
        body = await resp.json()

    assert body["detail"] == "Flight:unknown_flight_id not found."

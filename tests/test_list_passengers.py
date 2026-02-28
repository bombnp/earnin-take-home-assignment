import aiohttp


from tests.helpers import create_passenger


async def test_list_passengers_returns_created_booking(client: aiohttp.ClientSession):
    """My own additional edge case: Passengers appears in list after creation."""
    await create_passenger(client, "JFK003", "P001", "Alice", "Cooper")

    async with client.get("/flights/JFK003/passengers") as resp:
        assert resp.status == 200
        body = await resp.json()

    assert len(body["passengers"]) == 1

    passenger = body["passengers"][0]
    assert passenger["flight_id"] == "JFK003"
    assert passenger["passport_id"] == "P001"
    assert passenger["first_name"] == "Alice"
    assert passenger["last_name"] == "Cooper"


async def test_list_passengers_empty_for_flight_with_no_bookings(
    client: aiohttp.ClientSession,
):
    """My own additional edge case: No passengers booked on a flight"""
    async with client.get("/flights/CDG005/passengers") as resp:
        assert resp.status == 200
        body = await resp.json()

    assert body["passengers"] == []


async def test_list_passengers_isolation_between_flights(client: aiohttp.ClientSession):
    """My own additional edge case: Booking on one flight does not appear in another flight's passenger list."""
    await create_passenger(client, "LHR002", "P001", "Alice", "Cooper")

    async with client.get("/flights/DMK001/passengers") as resp:
        assert resp.status == 200
        body = await resp.json()

    passport_ids = [p["passport_id"] for p in body["passengers"]]
    assert "P001" not in passport_ids


async def test_list_passengers_multiple_bookings(client: aiohttp.ClientSession):
    """My own additional edge case: Multiple passengers on same flight all appear in the list."""
    await create_passenger(client, "SIN004", "P001", "Alice", "Cooper")
    await create_passenger(client, "SIN004", "P002", "Bob", "Smith")

    async with client.get("/flights/SIN004/passengers") as resp:
        assert resp.status == 200
        body = await resp.json()

    assert len(body["passengers"]) == 2
    passport_ids = {p["passport_id"] for p in body["passengers"]}
    assert passport_ids == {"P001", "P002"}

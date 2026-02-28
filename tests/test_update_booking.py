import aiohttp

from tests.helpers import create_passenger


async def test_update_passenger_successfully(client: aiohttp.ClientSession):
    """Scenario 5: Update customer contact information and flight details"""
    customer_id = await create_passenger(client, "DMK001", "P001", "Alice", "Cooper")

    update_payload = {
        "passport_id": "P002",
        "first_name": "Bob",
        "last_name": "Smith",
    }
    async with client.put(
        f"/flights/DMK001/passengers/{customer_id}", json=update_payload
    ) as resp:
        assert resp.status == 200
        body = await resp.json()

    assert body["flight_id"] == "DMK001"
    assert body["customer_id"] == customer_id
    assert body["passport_id"] == "P002"
    assert body["first_name"] == "Bob"
    assert body["last_name"] == "Smith"

    # list passenger's response should show updated passenger
    async with client.get("/flights/DMK001/passengers") as resp:
        assert resp.status == 200
        body = await resp.json()

    assert len(body["passengers"]) == 1
    passenger = body["passengers"][0]

    assert passenger["passport_id"] == "P002"
    assert passenger["first_name"] == "Bob"
    assert passenger["last_name"] == "Smith"


async def test_update_passenger_name_mismatch(client: aiohttp.ClientSession):
    """Scenario 6: Attempt to update customer name with mismatched details in Passport API"""
    customer_id = await create_passenger(client, "DMK001", "P001", "Alice", "Cooper")

    update_payload = {
        "passport_id": "P999",
        "first_name": "Alice",
        "last_name": "Cooper",
    }
    async with client.put(
        f"/flights/DMK001/passengers/{customer_id}", json=update_payload
    ) as resp:
        assert resp.status == 400
        body = await resp.json()

    assert body["detail"] == "Firstname or Lastname is mismatch."


async def test_update_nonexistent_passenger(client: aiohttp.ClientSession):
    """My own additional edge case: unknown passenger (customer id)"""
    update_payload = {
        "passport_id": "P001",
        "first_name": "Alice",
        "last_name": "Cooper",
    }
    async with client.put(
        "/flights/DMK001/passengers/999999", json=update_payload
    ) as resp:
        assert resp.status == 404
        body = await resp.json()

    assert "not found" in body["detail"].lower()


async def test_update_passenger_passport_not_found(client: aiohttp.ClientSession):
    """My own additional edge case: unknown passport id"""
    customer_id = await create_passenger(client, "DMK001", "P001", "Alice", "Cooper")

    update_payload = {
        "passport_id": "UNKNOWN_PASSPORT",
        "first_name": "Ghost",
        "last_name": "User",
    }
    async with client.put(
        f"/flights/DMK001/passengers/{customer_id}", json=update_payload
    ) as resp:
        assert resp.status == 400
        body = await resp.json()

    assert body["detail"] == "Passport not found."

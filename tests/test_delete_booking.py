import aiohttp


from tests.helpers import create_passenger


async def test_delete_booking_successfully(client: aiohttp.ClientSession):
    """Scenario 7: Delete a valid booking"""
    customer_id = await create_passenger(client, "SIN004", "P001", "Alice", "Cooper")

    async with client.delete(f"/flights/SIN004/passengers/{customer_id}") as resp:
        assert resp.status == 200 or resp.status == 204

    async with client.get("/flights/SIN004/passengers") as resp:
        assert resp.status == 200
        body = await resp.json()

    # customer should NOT appear in passengers list as booking is deleted
    customer_ids = [p["customer_id"] for p in body["passengers"]]
    assert customer_id not in customer_ids


async def test_delete_nonexistent_passenger(client: aiohttp.ClientSession):
    """My own additional edge case: Delete a passenger that does not exist, should return 404"""
    async with client.delete("/flights/SIN004/passengers/999999") as resp:
        assert resp.status == 404
        body = await resp.json()

    assert "not found" in body["detail"].lower()


async def test_delete_same_passenger_twice(client: aiohttp.ClientSession):
    """My own additional edge case: Deleting an already-deleted passenger, should return 404 on the second attempt."""
    customer_id = await create_passenger(client, "CDG005", "P002", "Bob", "Smith")

    async with client.delete(f"/flights/CDG005/passengers/{customer_id}") as resp:
        assert resp.status == 200

    async with client.delete(f"/flights/CDG005/passengers/{customer_id}") as resp:
        assert resp.status == 404

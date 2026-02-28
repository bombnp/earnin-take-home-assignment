import aiohttp


async def create_passenger(
    client: aiohttp.ClientSession,
    flight_id: str,
    passport_id: str,
    first_name: str,
    last_name: str,
) -> int:
    payload = {
        "passport_id": passport_id,
        "first_name": first_name,
        "last_name": last_name,
    }
    async with client.post(f"/flights/{flight_id}/passengers", json=payload) as resp:
        assert resp.status == 200, f"Setup failed: {await resp.text()}"
        body = await resp.json()
    return body["customer_id"]

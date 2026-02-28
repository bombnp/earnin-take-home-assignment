import aiohttp
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


async def test_list_flights_different_timezone(client: aiohttp.ClientSession):
    """Scenario 3: Retrieve flight details of the different timezone of departure and arrival airport."""
    async with client.get("/flights") as resp:
        assert resp.status == 200
        body = await resp.json()

    flights = {f["id"]: f for f in body["flights"]}
    assert "LHR002" in flights, "LHR002 must be present in seeded flights"

    flight = flights["LHR002"]
    departure_dt = datetime.fromisoformat(flight["departure_time"])
    arrival_dt = datetime.fromisoformat(flight["arrival_time"])

    # LHR002 UTC times from seed: departure 2025-03-10T10:00:00, arrival 2025-03-11T05:30:00
    dep_utc = datetime(2025, 3, 10, 10, 0, 0, tzinfo=timezone.utc)
    arr_utc = datetime(2025, 3, 11, 5, 30, 0, tzinfo=timezone.utc)

    expected_dep_offset = datetime.now(tz=ZoneInfo("Europe/London")).utcoffset()
    expected_arr_offset = datetime.now(tz=ZoneInfo("Asia/Bangkok")).utcoffset()

    assert departure_dt.utcoffset() == expected_dep_offset, (
        f"Departure should be in Europe/London offset {expected_dep_offset}, "
        f"got {departure_dt.utcoffset()}"
    )
    assert arrival_dt.utcoffset() == expected_arr_offset, (
        f"Arrival should be in Asia/Bangkok offset {expected_arr_offset}, "
        f"got {arrival_dt.utcoffset()}"
    )

    # Confirm they are different offsets
    assert departure_dt.utcoffset() != arrival_dt.utcoffset()

    # Confirm the UTC equivalent is preserved (timezone conversion doesn't shift the moment in time)
    assert departure_dt.astimezone(timezone.utc).replace(
        tzinfo=None
    ) == dep_utc.replace(tzinfo=None)
    assert arrival_dt.astimezone(timezone.utc).replace(tzinfo=None) == arr_utc.replace(
        tzinfo=None
    )


async def test_list_flights_same_timezone(client: aiohttp.ClientSession):
    """Scenario 4: Retrieve flight details of the same timezone of departure and arrival airport (Bangkok, ICT)"""
    async with client.get("/flights") as resp:
        assert resp.status == 200
        body = await resp.json()

    flights = {f["id"]: f for f in body["flights"]}
    assert "DMK001" in flights, "DMK001 must be present in seeded flights"

    flight = flights["DMK001"]
    departure_dt = datetime.fromisoformat(flight["departure_time"])
    arrival_dt = datetime.fromisoformat(flight["arrival_time"])

    # DMK001 UTC times from seed: departure 2025-03-10T01:00:00, arrival 2025-03-10T04:30:00
    dep_utc = datetime(2025, 3, 10, 1, 0, 0, tzinfo=timezone.utc)
    arr_utc = datetime(2025, 3, 10, 4, 30, 0, tzinfo=timezone.utc)

    expected_offset = datetime.now(tz=ZoneInfo("Asia/Bangkok")).utcoffset()

    assert departure_dt.utcoffset() == expected_offset, (
        f"Departure should be Asia/Bangkok offset {expected_offset}, "
        f"got {departure_dt.utcoffset()}"
    )
    assert arrival_dt.utcoffset() == expected_offset, (
        f"Arrival should be Asia/Bangkok offset {expected_offset}, "
        f"got {arrival_dt.utcoffset()}"
    )

    # Both timezones are the same
    assert departure_dt.utcoffset() == arrival_dt.utcoffset()

    # Confirm the UTC equivalent is preserved
    assert departure_dt.astimezone(timezone.utc).replace(
        tzinfo=None
    ) == dep_utc.replace(tzinfo=None)
    assert arrival_dt.astimezone(timezone.utc).replace(tzinfo=None) == arr_utc.replace(
        tzinfo=None
    )

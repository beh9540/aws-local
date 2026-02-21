import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.config import settings
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
@patch("app.main.ha_client.update_sensor", new_callable=AsyncMock)
async def test_receive_data_with_metadata(mock_update_sensor):
    # Setup settings for test
    settings.ambient_weather_passkey = "test_passkey"

    payload = {
        "PASSKEY": "test_passkey",
        "tempf": "72.5",
        "humidity": "45",
        "baromrelin": "29.92",
        "stationtype": "WS-2902"
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/data", params=payload)

    assert response.status_code == 200

    # Check calls to update_sensor
    # tempf
    mock_update_sensor.assert_any_call(
        "ambient_weather_tempf",
        72.5,
        {
            "friendly_name": "Outdoor Temperature",
            "unit_of_measurement": "°F",
            "device_class": "temperature",
            "state_class": "measurement",
            "unique_id": "test_passkey_tempf"
        }
    )

    # humidity
    mock_update_sensor.assert_any_call(
        "ambient_weather_humidity",
        45,
        {
            "friendly_name": "Outdoor Humidity",
            "unit_of_measurement": "%",
            "device_class": "humidity",
            "state_class": "measurement",
            "unique_id": "test_passkey_humidity"
        }
    )

    # baromrelin
    mock_update_sensor.assert_any_call(
        "ambient_weather_baromrelin",
        29.92,
        {
            "friendly_name": "Relative Barometer",
            "unit_of_measurement": "inHg",
            "device_class": "pressure",
            "state_class": "measurement",
            "unique_id": "test_passkey_baromrelin"
        }
    )

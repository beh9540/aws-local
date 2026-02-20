import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.config import settings
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
@patch("app.main.ha_client.update_sensor", new_callable=AsyncMock)
async def test_receive_data_success(mock_update_sensor):
    # Setup settings for test
    settings.ambient_weather_passkey = "test_passkey"
    
    payload = {
        "PASSKEY": "test_passkey",
        "tempf": "72.5",
        "humidity": "45",
        "stationtype": "WS-2902"
    }
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/data", params=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "ambient_weather_tempf" in response.json()["updated_sensors"]
    assert "ambient_weather_humidity" in response.json()["updated_sensors"]
    
    assert mock_update_sensor.call_count == 2

@pytest.mark.asyncio
async def test_receive_data_invalid_passkey():
    settings.ambient_weather_passkey = "correct_passkey"
    
    payload = {
        "PASSKEY": "wrong_passkey",
        "tempf": "72.5"
    }
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/data", params=payload)
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid PASSKEY"

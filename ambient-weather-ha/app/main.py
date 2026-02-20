from fastapi import FastAPI, Depends, HTTPException, Request
from .models import AmbientWeatherData
from .config import settings
from .ha_client import ha_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ambient Weather to Home Assistant Bridge")

@app.get("/data")
async def receive_ambient_data(request: Request):
    # WS-2902 sends data as query parameters in a GET request
    params = dict(request.query_params)
    
    try:
        data = AmbientWeatherData(**params)
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    if data.PASSKEY != settings.ambient_weather_passkey:
        logger.warning("Unauthorized access attempt with invalid PASSKEY")
        raise HTTPException(status_code=403, detail="Invalid PASSKEY")

    # Process and send to Home Assistant
    # We exclude PASSKEY and stationtype from being sensors
    exclude_fields = {"PASSKEY", "stationtype", "dateutc"}
    
    results = []
    for field, value in data.model_dump().items():
        if field not in exclude_fields and value is not None:
            sensor_id = f"{settings.sensor_prefix}_{field}"
            try:
                await ha_client.update_sensor(sensor_id, value, {"friendly_name": f"Ambient {field}"})
                results.append(sensor_id)
            except Exception as e:
                logger.error(f"Failed to update sensor {sensor_id}: {e}")

    return {"status": "success", "updated_sensors": results}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

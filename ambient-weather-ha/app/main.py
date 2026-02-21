from fastapi import FastAPI, HTTPException, Request
from .models import AmbientWeatherData
from .config import settings
from .ha_client import ha_client
from .metadata import SENSOR_METADATA
from typing import Any, cast
from contextlib import asynccontextmanager
import logging

# Set log level from settings
log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await ha_client.close()

app = FastAPI(title="Ambient Weather to Home Assistant Bridge", lifespan=lifespan)

@app.get("/data")
async def receive_ambient_data(request: Request):
    # WS-2902 sends data as query parameters in a GET request
    params = cast(Any, dict(request.query_params))
    
    logger.debug(f"Received request: {request.method} {request.url} Params: {params}")
    
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
            
            # Get metadata for this sensor
            metadata = SENSOR_METADATA.get(field)
            attributes = {}
            if metadata:
                attributes = {
                    "friendly_name": metadata.friendly_name,
                    "unit_of_measurement": metadata.unit_of_measurement,
                    "device_class": metadata.device_class,
                    "state_class": metadata.state_class,
                }
                # Remove None values
                attributes = {k: v for k, v in attributes.items() if v is not None}
            else:
                attributes = {"friendly_name": f"Ambient {field}"}

            try:
                await ha_client.update_sensor(sensor_id, value, attributes)
                results.append(sensor_id)
            except Exception as e:
                logger.error(f"Failed to update sensor {sensor_id}: {e}")

    return {"status": "success", "updated_sensors": results}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

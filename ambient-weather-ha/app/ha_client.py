import httpx
import logging
from typing import Any
from .config import settings

logger = logging.getLogger(__name__)

class HAClient:
    def __init__(self):
        self.base_url = settings.home_assistant_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.home_assistant_token}",
            "Content-Type": "application/json",
        }

    async def update_sensor(self, sensor_id: str, state: Any, attributes: dict = None):
        url = f"{self.base_url}/api/states/sensor.{sensor_id}"
        data = {
            "state": str(state),
            "attributes": attributes or {}
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error updating HA sensor {sensor_id}: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error updating HA sensor {sensor_id}: {e}")
                raise

ha_client = HAClient()

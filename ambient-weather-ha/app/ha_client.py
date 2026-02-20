import httpx
import logging
from typing import Any, Optional
from .config import settings

logger = logging.getLogger(__name__)

class HAClient:
    def __init__(self):
        self.base_url = settings.home_assistant_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.home_assistant_token}",
            "Content-Type": "application/json",
        }
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(headers=self.headers)
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def update_sensor(self, sensor_id: str, state: Any, attributes: Optional[dict] = None):
        url = f"{self.base_url}/api/states/sensor.{sensor_id}"
        data = {
            "state": str(state),
            "attributes": attributes or {}
        }
        
        try:
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Error updating HA sensor {sensor_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error updating HA sensor {sensor_id}: {e}")
            raise

ha_client = HAClient()

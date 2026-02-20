from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    home_assistant_url: str = Field(..., alias="HOME_ASSISTANT_URL")
    home_assistant_token: str = Field(..., alias="HOME_ASSISTANT_TOKEN")
    ambient_weather_passkey: str = Field(..., alias="AMBIENT_WEATHER_PASSKEY")
    
    # Optional: prefix for Home Assistant sensors
    sensor_prefix: str = Field("ambient_weather", alias="SENSOR_PREFIX")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

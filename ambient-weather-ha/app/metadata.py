from typing import Dict, Optional
from pydantic import BaseModel

class SensorMetadata(BaseModel):
    friendly_name: str
    unit_of_measurement: Optional[str] = None
    device_class: Optional[str] = None
    state_class: Optional[str] = "measurement"

SENSOR_METADATA: Dict[str, SensorMetadata] = {
    "tempf": SensorMetadata(
        friendly_name="Outdoor Temperature",
        unit_of_measurement="°F",
        device_class="temperature"
    ),
    "humidity": SensorMetadata(
        friendly_name="Outdoor Humidity",
        unit_of_measurement="%",
        device_class="humidity"
    ),
    "tempinf": SensorMetadata(
        friendly_name="Indoor Temperature",
        unit_of_measurement="°F",
        device_class="temperature"
    ),
    "humidityin": SensorMetadata(
        friendly_name="Indoor Humidity",
        unit_of_measurement="%",
        device_class="humidity"
    ),
    "baromrelin": SensorMetadata(
        friendly_name="Relative Barometer",
        unit_of_measurement="inHg",
        device_class="pressure"
    ),
    "baromabsin": SensorMetadata(
        friendly_name="Absolute Barometer",
        unit_of_measurement="inHg",
        device_class="pressure"
    ),
    "windspeedmph": SensorMetadata(
        friendly_name="Wind Speed",
        unit_of_measurement="mph",
        device_class="wind_speed"
    ),
    "windgustmph": SensorMetadata(
        friendly_name="Wind Gust Speed",
        unit_of_measurement="mph",
        device_class="wind_speed"
    ),
    "winddir": SensorMetadata(
        friendly_name="Wind Direction",
        unit_of_measurement="°"
    ),
    "rainin": SensorMetadata(
        friendly_name="Rain Rate",
        unit_of_measurement="in/h",
        device_class="precipitation_intensity"
    ),
    "dailyrainin": SensorMetadata(
        friendly_name="Daily Rain",
        unit_of_measurement="in",
        device_class="precipitation",
        state_class="total_increasing"
    ),
    "weeklyrainin": SensorMetadata(
        friendly_name="Weekly Rain",
        unit_of_measurement="in",
        device_class="precipitation",
        state_class="total_increasing"
    ),
    "monthlyrainin": SensorMetadata(
        friendly_name="Monthly Rain",
        unit_of_measurement="in",
        device_class="precipitation",
        state_class="total_increasing"
    ),
    "yearlyrainin": SensorMetadata(
        friendly_name="Yearly Rain",
        unit_of_measurement="in",
        device_class="precipitation",
        state_class="total_increasing"
    ),
    "solarradiation": SensorMetadata(
        friendly_name="Solar Radiation",
        unit_of_measurement="W/m²",
        device_class="irradiance"
    ),
    "uv": SensorMetadata(
        friendly_name="UV Index",
        unit_of_measurement="UV Index"
    ),
    "last_rain_dateutc": SensorMetadata(
        friendly_name="Last Rain Date",
        device_class="timestamp",
        state_class=None
    ),
    "feelsLike": SensorMetadata(
        friendly_name="Feels Like",
        unit_of_measurement="°F",
        device_class="temperature"
    ),
    "dewPoint": SensorMetadata(
        friendly_name="Dew Point",
        unit_of_measurement="°F",
        device_class="temperature"
    )
}

from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class AmbientWeatherData(BaseModel):
    # Standard fields sent by WS-2902
    PASSKEY: str
    stationtype: Optional[str] = None
    dateutc: Optional[str] = None
    tempf: Optional[float] = None
    humidity: Optional[int] = None
    windspeedmph: Optional[float] = None
    windgustmph: Optional[float] = None
    winddir: Optional[int] = None
    rainin: Optional[float] = None
    dailyrainin: Optional[float] = None
    weeklyrainin: Optional[float] = None
    monthlyrainin: Optional[float] = None
    yearlyrainin: Optional[float] = None
    solarradiation: Optional[float] = None
    uv: Optional[int] = None
    baromrelin: Optional[float] = None
    baromabsin: Optional[float] = None
    tempinf: Optional[float] = None
    humidityin: Optional[int] = None
    
    model_config = ConfigDict(extra="allow")

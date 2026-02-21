# Ambient Weather WS-2902 to Home Assistant Bridge

This is a FastAPI application that receives data from an Ambient Weather WS-2902 weather station and forwards it to Home Assistant.

## Features
- FastAPI for high performance
- Pydantic for robust configuration and data validation
- `uv` for lightning-fast dependency management
- Multi-stage Dockerfile with automated tests
- Unit tests with `pytest`

## Configuration
Copy `.env.example` to `.env` and fill in your details:
- `HOME_ASSISTANT_URL`: The URL of your Home Assistant instance (e.g., `http://192.168.1.10:8123`).
- `HOME_ASSISTANT_TOKEN`: A Long-Lived Access Token generated in Home Assistant.
- `AMBIENT_WEATHER_PASSKEY`: The MAC address or PASSKEY of your weather station (found in the AWnet app or AmbientWeather.net).
- `SENSOR_PREFIX`: Optional prefix for your sensors (defaults to `ambient_weather`).

## Running with Docker
```bash
docker build -t ambient-weather-ha .
docker run -p 8000:8000 --env-file .env ambient-weather-ha
```

## Weather Station Setup
In the AWnet app or your station's web interface, set up a "Custom Server":
- **Server IP/Hostname**: The IP address of the machine running this bridge.
- **Path**: `/data`
- **Port**: `8000`
- **Interval**: `60` (or your preferred interval)

## Development
```bash
uv sync
uv run uvicorn app.main:app --reload
```

## Testing and Linting
We use `tox` for running all checks in a consistent environment.

### Running all checks (Tests, Linting, Type-checking)
```bash
uv run tox
```

### Individual checks
You can run individual environments with `tox -e`:
```bash
uv run tox -e lint        # Run ruff check
uv run tox -e typecheck   # Run ty check
uv run tox -e py311       # Run pytest
```

## Pre-commit Hooks
This project uses `pre-commit` to ensure code quality before each commit. To install the hooks:
```bash
uv run pre-commit install
```
Once installed, `tox` will run automatically on every commit. You can also run it manually:
```bash
uv run pre-commit run --all-files
```

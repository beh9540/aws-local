# AWS Local Setup
Local development and bridge for AWS-connected devices and services.

## Ambient Weather WS-2902 to Home Assistant Bridge
The main component currently is the bridge for Ambient Weather stations.

See the [Ambient Weather HA README](./ambient-weather-ha/README.md) for detailed instructions on setup, configuration, and development.

### Quick Start
1.  Navigate to the project directory: `cd ambient-weather-ha`
2.  Install dependencies: `uv sync`
3.  Install pre-commit hooks: `uv run pre-commit install`
4.  Run all checks with tox: `uv run tox`

# HealthPi — IoT Vehicle Health Monitoring and Diagnostics

HealthPi is an IoT-based vehicle health monitoring and diagnostics prototype. The project collects vehicle-related sensor values, sends telemetry to ThingSpeak, uses a Random Forest machine-learning model to classify vehicle condition, and sends status notifications through Telegram.

## Project flow

```text
Sensors / Arduino UNO
        |
        v
   ThingSpeak
        |
        v
 Python prediction service
        |
        +--> Random Forest model
        |
        +--> Vehicle status
                |
                v
             Telegram
```

## Hardware prototype

The prototype uses an Arduino UNO with an LCD, temperature/environment sensors, pressure sensing, an analog throttle input, an IR-based RPM input, a buzzer, and a motor/wheel assembly.

See [`docs/hardware.jpg`](docs/hardware.jpg).

## Software components

- `hardware/vh_mntrng.ino` — Arduino/IoT firmware.
- `ml/ds.py` — generates the sample vehicle monitoring dataset.
- `ml/train.py` — trains a Random Forest classifier and saves the model.
- `ml/pred.py` — reads the latest ThingSpeak values, predicts vehicle status, and sends Telegram notifications.
- `ml/vehicle_monitoring_data.csv` — generated sample dataset.
- `ml/vehicle_monitoring_model.pkl` — trained model artifact.

## Input features used by the ML model

The model uses:

1. Engine temperature
2. Runtime
3. Throttle
4. RPM

The training code maps the target to three statuses:

- `0` — Normal
- `1` — Needs Maintenance
- `2` — Abnormal Condition

## Arduino telemetry mapping

The current firmware sends the following values to ThingSpeak in order:

- Field 1 — engine temperature from the Dallas temperature sensor
- Field 2 — DHT temperature
- Field 3 — DHT humidity
- Field 4 — runtime
- Field 5 — throttle value
- Field 6 — pressure value
- Field 7 — RPM

The prediction service currently consumes fields 1, 4, 5, and 7.

## Local setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the model

```bash
cd ml
python ds.py
python train.py
```

### 4. Configure Telegram

Copy `.env.example` to `.env` and set your Telegram credentials.

For production, prefer environment variables or GitHub/hosting secrets rather than committing `.env`.

### 5. Run prediction service

From the `ml` directory:

```bash
python pred.py
```

The prediction service checks ThingSpeak every 20 seconds.

## Arduino setup

Install the Arduino libraries required by the firmware, including:

- LiquidCrystal
- DHT sensor library
- OneWire
- DallasTemperature
- Adafruit BMP085/BMP180 library

Before uploading the sketch, replace the placeholder `THINGSPEAK_WRITE_API_KEY` with your actual ThingSpeak write API key locally. Do not commit that key to GitHub.

## GitHub Actions

The workflow in `.github/workflows/python-ci.yml` automatically:

1. Installs Python dependencies.
2. Compiles the Python source files.
3. Generates the sample dataset.
4. Trains the model.

It runs on pushes and pull requests targeting `main`.

## Manual GitHub commands

Create an empty GitHub repository named `HealthPi`, then run from this directory:

```bash
git init
git add .
git commit -m "Initial commit - HealthPi vehicle monitoring"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/HealthPi.git
git push -u origin main
```

For later changes:

```bash
git add .
git commit -m "Update HealthPi"
git push
```

## Security note

Never commit API keys, bot tokens, passwords, or other credentials. If a credential has already been exposed in a public or shared repository, revoke/regenerate it before publishing the project.

## Project status

This repository represents the current prototype and its existing data/ML workflow. Hardware-to-cloud transport and the ML prediction pipeline should be tested with the actual hardware and ThingSpeak channel before production use.

# 3D LIDAR Scanner

Builds a 3D point cloud by rotating an RPLiDAR A1M8 on a stepper motor mount controlled by a Raspberry Pi + Arduino. The LIDAR captures 2D scan slices while the stepper tilts the sensor; the combined data produces a 3D representation of the environment.

## Architecture

```
RPLiDAR A1M8 ──USB──▶ Raspberry Pi (Python)
                         │
                         │ serial/GPIO
                         ▼
                      Arduino ──▶ Stepper motor (tilts the LIDAR)

Scan slices + angle ──▶ 3D point cloud ──▶ visualisation
```

## Directory Structure

| Directory | Description |
|---|---|
| `lidar/` | LIDAR subsystem — raw scan capture, graphic display, start/stop scripts |
| `servo/` | Motor subsystem — stepper driver (Arduino sketches + Python interface), servo tests, homing |
| `combined/` | Integrated system — `StepModule.py` (stepper driver), `test_1.py` / `test_2.py` (combined scan routines) |
| `visualisation/` | Point cloud visualisation and anomaly detection |
| `Ref/` | GPIO reference images, Adafruit RPLiDAR library, SLAMTEC RPLiDAR SDK |

## Hardware

| Component | Role |
|---|---|
| RPLiDAR A1M8 (SLAMTEC) | 2D laser scanner (360-degree, ~8000 samples/s) |
| Raspberry Pi | Main controller, runs Python scan scripts |
| Arduino | Stepper motor driver (receives serial commands from Pi) |
| Stepper motor + mount | Tilts LIDAR for 3D scanning |
| Homing switch | Reference position for stepper motor |

## Requirements

```bash
pip install rplidar-roboticia numpy matplotlib
```

Arduino libraries: AccelStepper

## Usage

```bash
cd combined
python test_1.py
```

## Branches

| Branch | Description |
|---|---|
| `main` | Current integrated code |
| `addstepmotor` | Stepper motor integration work |
| `simplify-arduino` | Simplified Arduino driver |

## Known Issues

See `to do.md` for the full list. Key items:
- LIDAR resolution may be limited by scan rate — check sensor configuration
- Stepper vibration addressed but motor command/receive decoupling still needed
- Mount plate may block LIDAR line of sight at low angles

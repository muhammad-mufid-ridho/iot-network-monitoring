# Industrial IoT Monitoring Platform
### ESP32 Telemetry Monitoring with MQTT, Python, Prometheus & Grafana

**Project Type:** Internet of Things (IoT) / Network Monitoring  
**Status:** Prototype – Functional  
**Development Environment:** Windows, Docker, Python, Wokwi  
**Date:** November 2026

## 2. Dashboard Preview

![IoT Monitoring Dashboard](docs/screenshots/grafana-dashboard.png)

*Grafana dashboard displaying ESP32 device status, telemetry age, received messages, uptime, and telemetry rate.*

## 1. Project Overview

This project is a prototype IoT monitoring platform designed to collect, process, and visualize telemetry data from an ESP32 device in near real time.

The system uses MQTT for device communication, Python as the monitoring engine, Prometheus for metrics collection, and Grafana for dashboard visualization.

The main objective is to demonstrate how IoT device telemetry can be monitored, how device communication interruptions can be detected, and how operational metrics can be presented through a centralized dashboard.

## 2. System Architecture

```text
ESP32 (Wokwi Simulator)
        |
        | MQTT Telemetry
        v
HiveMQ Public MQTT Broker
        |
        | MQTT Subscription
        v
Python Monitoring Engine
        |
        | Prometheus Metrics
        v
Prometheus Server (Docker)
        |
        | PromQL
        v
Grafana Dashboard
```

## 3. Technologies Used

| Technology | Function |
|---|---|
| ESP32 / Wokwi | Simulated IoT device |
| MQTT / HiveMQ | Telemetry communication |
| Python | MQTT subscriber and monitoring engine |
| Paho MQTT | Python MQTT client |
| Prometheus Client | Exposes monitoring metrics |
| Prometheus | Metrics collection and querying |
| Grafana | Dashboard visualization |
| Docker Compose | Runs supporting services |
| PowerShell | Windows environment management |

## 4. Implemented Features

- ESP32 publishes JSON telemetry every 5 seconds.
- Python subscribes to MQTT telemetry.
- Incoming messages are parsed and validated.
- Prometheus metrics are exposed through HTTP port 8000.
- Prometheus scrapes the Python exporter every 5 seconds.
- Device availability is evaluated using a 15-second telemetry timeout.
- Grafana visualizes device status, telemetry age, total messages, device uptime, and telemetry rate.
- Device interruption and recovery can be demonstrated by stopping and restarting the Wokwi simulation.

## 5. Monitoring Metrics

| Metric | Description |
|---|---|
| `iot_device_up` | Device telemetry availability (1 = UP, 0 = DOWN) |
| `iot_telemetry_age_seconds` | Age of the latest received telemetry |
| `iot_messages_received_total` | Total telemetry messages received |
| `iot_device_uptime_ms` | Device-reported uptime |
| `iot_last_sequence` | Last received message sequence |
| `iot_last_message_timestamp_seconds` | Timestamp of latest received message |

## 6. Dashboard

The Grafana dashboard, named **New ESP32 Device Status**, provides a centralized view of the ESP32 telemetry monitoring system.

Dashboard panels include:

1. ESP32 Device Status
2. Telemetry Age
3. Total Telemetry Received
4. ESP32 Device Uptime
5. Telemetry Rate
6. Telemetry Rate History (if enabled and saved)

## 7. Testing and Validation

The prototype was tested through the following scenarios:

- Verified MQTT connection between ESP32 simulation and HiveMQ.
- Verified telemetry reception by the Python monitoring engine.
- Verified Prometheus metrics through the `/metrics` endpoint.
- Verified Prometheus target availability.
- Queried telemetry metrics using PromQL.
- Stopped the ESP32 simulation and observed the device status change to DOWN after the timeout.
- Restarted the simulation and verified telemetry recovery.

## 8. Project Limitations and Future Improvements

This implementation is a functional prototype, not yet a production-ready industrial monitoring system.

Planned improvements:

- ICMP and TCP network latency monitoring.
- Packet loss and jitter measurement.
- DNS and MQTT connectivity diagnostics.
- Alerting and notification integration.
- MQTT authentication and TLS encryption.
- Multi-device and multi-site monitoring.
- Docker-based deployment documentation.
- Automated testing and fault simulation.

**Security note:** The current demonstration uses a public HiveMQ broker over MQTT port 1883. It is intended for non-sensitive test telemetry only. Production deployment requires authenticated and encrypted communication.

## 9. Project Outcome

A working end-to-end IoT telemetry monitoring prototype was successfully developed. The implementation demonstrates device-to-cloud MQTT communication, Python-based telemetry processing, Prometheus metrics exposition and collection, and Grafana dashboard visualization.

The project establishes a foundation for developing a more comprehensive industrial IoT monitoring and network diagnostics platform.

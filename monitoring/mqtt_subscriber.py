
import json
import time
import threading

import paho.mqtt.client as mqtt

from prometheus_client import (
    start_http_server,
    Counter,
    Gauge
)

# ==========================================
# 1. KONFIGURASI
# ==========================================

MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883

MQTT_TOPIC = (
    "iot-monitoring/demo-7f3a/"
    "site01/esp32-001/telemetry"
)

DEVICE_ID = "esp32-001"

PROMETHEUS_PORT = 8000
DEVICE_TIMEOUT = 15  # detik


# ==========================================
# 2. PROMETHEUS METRICS
# ==========================================

messages_received = Counter(
    "iot_messages_received",
    "Total MQTT telemetry messages received",
    ["device_id"]
)

device_up = Gauge(
    "iot_device_up",
    "Device telemetry availability (1=UP, 0=DOWN)",
    ["device_id"]
)

device_uptime = Gauge(
    "iot_device_uptime_ms",
    "Device uptime in milliseconds",
    ["device_id"]
)

last_sequence = Gauge(
    "iot_last_sequence",
    "Last received MQTT sequence number",
    ["device_id"]
)

last_message_timestamp = Gauge(
    "iot_last_message_timestamp_seconds",
    "Unix timestamp of last received telemetry",
    ["device_id"]
)

telemetry_age = Gauge(
    "iot_telemetry_age_seconds",
    "Age of the latest telemetry in seconds",
    ["device_id"]
)


# ==========================================
# 3. INITIAL STATE
# ==========================================

last_message_time = 0

device_up.labels(DEVICE_ID).set(0)


# ==========================================
# 4. MQTT CALLBACKS
# ==========================================

def on_connect(client, userdata, flags, reason_code, properties):

    if reason_code == 0:
        print("[CONNECTED] HiveMQ connection successful")

        client.subscribe(MQTT_TOPIC)

        print(f"[SUBSCRIBED] {MQTT_TOPIC}")

    else:
        print(f"[ERROR] MQTT connection failed: {reason_code}")


def on_message(client, userdata, message):

    global last_message_time

    try:
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)

        device_id = data["device_id"]
        status = data["status"]
        uptime_ms = int(data["uptime_ms"])
        sequence = int(data["sequence"])

        received_time = time.time()

        last_message_time = received_time

        # Update Prometheus metrics
        messages_received.labels(device_id).inc()

        device_up.labels(device_id).set(1)

        device_uptime.labels(device_id).set(uptime_ms)

        last_sequence.labels(device_id).set(sequence)

        last_message_timestamp.labels(device_id).set(
            received_time
        )

        telemetry_age.labels(device_id).set(0)

        print("\n========== TELEMETRY ==========")
        print(f"Device ID : {device_id}")
        print(f"Status    : {status}")
        print(f"Uptime    : {uptime_ms} ms")
        print(f"Sequence  : {sequence}")
        print("================================")

    except (ValueError, KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"[ERROR] Invalid telemetry: {error}")


# ==========================================
# 5. DEVICE HEALTH MONITOR
# ==========================================

def monitor_device_health():

    global last_message_time

    while True:

        if last_message_time == 0:
            age = 0
            device_up.labels(DEVICE_ID).set(0)

        else:
            age = time.time() - last_message_time

            telemetry_age.labels(DEVICE_ID).set(age)

            if age > DEVICE_TIMEOUT:
                device_up.labels(DEVICE_ID).set(0)
                print("[WARNING] ESP32 telemetry timeout!")

            else:
                device_up.labels(DEVICE_ID).set(1)

        time.sleep(1)


# ==========================================
# 6. START MONITORING ENGINE
# ==========================================

if __name__ == "__main__":

    print("[START] IoT Monitoring Engine")

    # Start Prometheus HTTP endpoint
    start_http_server(PROMETHEUS_PORT)

    print(
        f"[PROMETHEUS] http://localhost:"
        f"{PROMETHEUS_PORT}/metrics"
    )

    # Start health monitoring thread
    health_thread = threading.Thread(
        target=monitor_device_health,
        daemon=True
    )

    health_thread.start()

    # Create MQTT client
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="python-monitor-esp32-001"
    )

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(
            MQTT_HOST,
            MQTT_PORT,
            keepalive=60
        )

        client.loop_forever()

    except KeyboardInterrupt:
        print("\n[STOP] Monitoring stopped")
        client.disconnect()

    except Exception as error:
        print(f"[ERROR] {error}")

import datetime
import time
import json
import paho.mqtt.client as mqtt
import threading
from xiaomi_gateway import XiaomiGatewayDiscovery, _validate_data

MQTT_BROKER_URI = "localhost"

gateways_config = [
    {
        # 'disable': 'false',
        'host': '10.3.141.20',
        'port': '9898',
        'sid': '7811dcfb0bc6',
        'key': 'fd27vp05jmnngcz2'
    }
]

lock = threading.Lock()

def parse_data(data, data_mqtt):
    for key in data:
        value = data[key]
        # XiaomiDevice
        if key in ['voltage', "battery_voltage"]:
            data_mqtt['voltage'] = round(value / 1000.0, 3)
        # XiaomiSensor
        elif key in ["status"]:
            if value == "close":
                data_mqtt[key] = 1
            else:
                data_mqtt[key] = 0
        elif key in ["temperature", "humidity", "pressure"]:
            data_mqtt[key] = float(value) / 100
        # General
        else:
            data_mqtt[key] = value

def publish_sensor_data_to_mqtt(gateway, sensor):
    with lock:
        now = datetime.datetime.now()
        client = mqtt.Client("mihome_to_mqtt_" + now.strftime("%Y-%m-%d_%H:%M:%S"))
        client.connect(MQTT_BROKER_URI)
        topic = f'mihome/{sensor.get("model")}/{gateway.sid}/{sensor.get("sid")}'
        data = sensor['data']
        data_mqtt = {}
        parse_data(data, data_mqtt)
        data_str = json.dumps(data_mqtt)
        print(f'MQTT {client._bind_address} {topic} {data_str}')
        info = client.publish(topic, data_str)
        info.wait_for_publish()
        time.sleep(1) # Fixes OpenHAB MQTT Broker errors
        client.disconnect()

def update_sensor_data(gateway, sensor, data_report, is_report=False):
    data = sensor['data']
    print(f'sensor data = {data}')
    if is_report:
        now = datetime.datetime.now()
        data['changed'] = now.strftime("%Y-%m-%d %H:%M:%S")
    for key, value in data_report.items():
        data[key] = value
    print(f'sensor data new = {sensor["data"]}')
    publish_sensor_data_to_mqtt(gateway, sensor)


def report_callback(push_data, report):
    # POZOR: PORAD TAM JDOU DATA I Z GATEWAY !!!
    # REPORT - {'cmd': 'report', 'model': 'gateway', 'sid': '7811dcfb0bc6', 'short_id': 0, 'data': '{"rgb":0,"illumination":1117}'}
    # UNKNOWN DEVICE sid = 7811dcfb0bc6
    if ((report is None) or not ('cmd' in report) or not ('sid' in report) or not ('data' in report)) or not (report['cmd'] in ['report', 'heartbeat']):
        print(f'REPORT INVALID: {report}')
        return
    try:
        print(f'REPORT - {report}')
        sensor_id = report['sid']
        data_report = json.loads(report['data'])
        # Update device data from given report
        for _, gateway in mihome.gateways.items():
            if not sensor_id in gateway.sensors:
                print(f'UNKNOWN DEVICE sid = {sensor_id}')
            else:
                sensor = gateway.sensors[sensor_id]
                update_sensor_data(gateway, sensor, data_report, True)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly, but may be overridden in exception subclasses


mihome = XiaomiGatewayDiscovery(report_callback, gateways_config, 'any')
mihome.discover_gateways()
for host, gateway in mihome.gateways.items():
    print(f'GATEWAY [{host}] - SENSOR DISCOVERED:')
    for sensor_id, sensor in gateway.sensors.items():
        print(f'{sensor_id} - {sensor}')
mihome.listen()
while True:
    time.sleep(10)
    for host, gateway in mihome.gateways.items():
        print(f'---GATEWAY [{host}]: token: {gateway.token}')
        for sensor_id, sensor in gateway.sensors.items():
            cmd = '{"cmd":"read","sid":"' + sensor_id + '"}'
            resp = gateway._send_cmd(cmd, "read_ack") if int(
                gateway.proto[0:1]) == 1 else gateway._send_cmd(cmd, "read_rsp")
            if _validate_data(resp):
                data_report = sensor['data']
                update_sensor_data(gateway, sensor, data_report)



# for config in gws_config:
#     host = config.get('host')
#     print(gwd.gateways.items())
#     print(gwd.gateways[host])
#     gw = gwd.gateways[host]
#     print(gw)
#     print(gw.devices)

# for host, gw in gwd.gateways.items():
#     print(f'{host} - {gw}')
#     for device_type, xiaomi_device in gw.devices.items():
#         print('***')
#         print(f'{device_type} - {xiaomi_device}')

# for host, gw in gwd.gateways.items():
#     for device in gw.sensors:
#         print('***')
#         print(device)

# gwd.listen()
# while True:
#     time.sleep(20)
#     gwd.stop_listen()
#     while gwd._listening:
#         time.sleep(1)
#     gwd.discover_gateways()
#     gwd.listen()

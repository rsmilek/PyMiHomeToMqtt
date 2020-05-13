import time
import json
from xiaomi_gateway import XiaomiGatewayDiscovery

gateways_config = [
    {
        # 'disable': 'false',
        'host': '10.3.141.20',
        'port': '9898',
        'sid': '7811dcfb0bc6',
        'key': 'fd27vp05jmnngcz2'
    }
]


def report_callback(push_data, report):
    # POZOR: PORAD TAM JDOU DATA I Z GATEWAY !!!
    if ((report is None) or not ('cmd' in report) or not ('sid' in report) or not ('data' in report)) or not (report['cmd'] in ['report', 'heartbeat']):
        print(f'REPORT INVALID: {report}')
        return
    try:
        print(f'REPORT - {report}')
        sensor_id = report['sid']
        data_report = json.loads(report['data'])
        for key, value in data_report.items():
            # print(f'report data: key = {key} : value = {value}')
            for _, gateway in mihome.gateways.items():
                if not sensor_id in gateway.sensors:
                    print(f'UNKNOWN DEVICE sid = {sensor_id}')
                    return
                sensor = gateway.sensors[sensor_id]
                data = sensor['data']
                print(f'sensor data = {data}')
                data[key] = value
                print(f'sensor data new = {sensor["data"]}')
        # info = {}
        #     info[key] = value
        # print(f'info = {info}')

    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        # __str__ allows args to be printed directly, but may be overridden in exception subclasses
        print(inst)


mihome = XiaomiGatewayDiscovery(report_callback, gateways_config, 'any')
mihome.discover_gateways()

for host, gateway in mihome.gateways.items():
    for sensor_id, sensor in gateway.sensors.items():
        print('***')
        print(f'{sensor_id} - {sensor}')
mihome.listen()
while True:
    time.sleep(10)


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

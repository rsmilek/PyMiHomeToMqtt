import time
from xiaomi_gateway import XiaomiGatewayDiscovery

gw_config = {
    # 'disable': 'false',
    'host': '10.3.141.20',
    'port': '9898',
    'sid': '7811dcfb0bc6',
    'key': 'fd27vp05jmnngcz2'
}

gws_config = [gw_config]

gwd = XiaomiGatewayDiscovery(lambda: None, [gw_config], 'any')
gwd.discover_gateways()


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

for host, gw in gwd.gateways.items():
    for sid, sensor in gw.sensors.items():
        print('***')
        print(f'{sid} - {sensor}')


# gwd.listen()
# while True:
#     time.sleep(20)
#     gwd.stop_listen()
#     while gwd._listening:
#         time.sleep(1)
#     gwd.discover_gateways()
#     gwd.listen()

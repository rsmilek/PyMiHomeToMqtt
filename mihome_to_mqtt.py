import time
from xiaomi_gateway import XiaomiGatewayDiscovery

gw_config = {
    # 'disable': 'false',
    'host': '10.3.141.20',
    'port': '9898',
    'sid': '7811dcfb0bc6',
    'key': 'fd27vp05jmnngcz2'
}

gwd = XiaomiGatewayDiscovery(lambda: None, [gw_config], 'any')
gwd.discover_gateways()
gwd.listen()
while True:
    time.sleep(20)
    gwd.stop_listen()
    while gwd._listening:
        time.sleep(1)
    gwd.discover_gateways()
    gwd.listen()

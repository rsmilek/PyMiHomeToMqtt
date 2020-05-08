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
    print("This prints once a minute.")
    time.sleep(60)  # Delay for 1 minute (60 seconds).

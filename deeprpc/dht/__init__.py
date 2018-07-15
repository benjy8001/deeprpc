import os
import asyncio
from pickle import dumps, loads
import logging

from kademlia.network import Server


__version__ = "0.1"

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)


BOOSTRAP_IP = os.getenv('BOOSTRAP_IP', 'bootstrap')
BOOSTRAP_PORT = int(os.getenv('BOOSTRAP_PORT', 8000))
UDHT_PORT = int(os.getenv('UDHT_PORT', 9000))

BOOTSTRAP_NODE = (BOOSTRAP_IP, BOOSTRAP_PORT)


class Empty(object):
    pass


class DHT:
    """docstring for Server"""
    def __init__(self, ip_address=BOOSTRAP_IP, port=BOOSTRAP_PORT):
        self.server = Server()
        self.server.listen(UDHT_PORT)

        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)

        bootstrap_node = (ip_address, int(port))
        self.loop.run_until_complete(self.server.bootstrap([bootstrap_node]))

    def stop(self):
        self.server.stop()
        self.loop.close()

    def __getitem__(self, key):
        result = Empty()
        try:
            result = loads(self.loop.run_until_complete(self.server.get(key)))
        except TypeError:
            pass
        if isinstance(result, Empty):
            raise KeyError

        return result

    def __setitem__(self, key, item):
        self.loop.run_until_complete(self.server.set(key, dumps(item)))

    def __delitem__(self, key):
        self.loop.run_until_complete(self.server.set(key, dumps(Empty())))

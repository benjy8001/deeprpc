import os
import asyncio
from pickle import dumps, loads

from kademlia.network import Server as BaseServer
from kademlia.protocol import KademliaProtocol
from kademlia.utils import digest
from kademlia.storage import ForgetfulStorage
from kademlia.node import Node
from kademlia.crawling import ValueSpiderCrawl
from kademlia.crawling import NodeSpiderCrawl

from deeprpc.dht.protocol import Protocol

import logging

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


class Server(BaseServer):

    protocol_class = Protocol

    async def find_neighbors_nodes(self, key):
        dkey = digest(key)

        return await self._find_neighbors_nodes(dkey)

    async def _find_neighbors_nodes(self, dkey):
        node = Node(dkey)

        nearest = self.protocol.router.findNeighbors(node)
        if len(nearest) == 0:
            log.warning("There are no known neighbors to set key %s",
                        dkey.hex())
            return False

        spider = NodeSpiderCrawl(self.protocol, node, nearest,
                                 self.ksize, self.alpha)
        nodes = await spider.find()

        return nodes

    async def something(self):
        from uuid import uuid4
        random_key = str(uuid4())

        nodes = await self.find_neighbors_nodes(random_key)

        d = self.protocol.callSomething(nodes[0], 'foo', 'bar')
        return await asyncio.gather(d)

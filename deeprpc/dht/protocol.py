from kademlia.protocol import KademliaProtocol as BaseProtocol
from kademlia.node import Node


class Protocol(BaseProtocol):
    def rpc_dosomething(self, sender, nodeid, foo, bar):
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)

        return dict(foo=foo, bar=bar)

    async def callSomething(self, nodeToAsk, foo, bar):
        address = (nodeToAsk.ip, nodeToAsk.port)
        result = await self.dosomething(address, self.sourceNode.id, foo, bar)
        return self.handleCallResponse(result, nodeToAsk)

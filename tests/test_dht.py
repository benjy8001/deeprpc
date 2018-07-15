import os

BOOSTRAP_IP = os.getenv('BOOSTRAP_IP', 'bootstrap')
BOOSTRAP_PORT = int(os.getenv('BOOSTRAP_PORT', 8000))
UDHT_PORT = int(os.getenv('UDHT_PORT', 9000))

BOOTSTRAP_NODE = (BOOSTRAP_IP, BOOSTRAP_PORT)


def test_something():
    import asyncio

    from deeprpc.dht.server import Server

    server = Server()
    server.listen(UDHT_PORT)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.bootstrap([BOOTSTRAP_NODE]))
    result = loop.run_until_complete(server.something())

    assert len(result) == 1
    assert result[0][0]
    assert result[0][1] == dict(foo='foo', bar='bar')

import logging
import os
import asyncio

from deeprpc.dht.server import Server


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


def main():

    server = Server()
    server.listen(UDHT_PORT)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.bootstrap([BOOTSTRAP_NODE]))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


if __name__ == '__main__':
    main()

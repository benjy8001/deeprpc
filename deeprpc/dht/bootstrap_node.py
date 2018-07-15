import os
import asyncio

import logging

from deeprpc.dht.server import Server

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)


BOOSTRAP_PORT = int(os.getenv('BOOSTRAP_PORT', 8000))


def main():
    server = Server()
    server.listen(BOOSTRAP_PORT)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


if __name__ == '__main__':
    main()

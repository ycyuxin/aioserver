import asyncio
import logging
from asyncio import DatagramTransport
from typing import Tuple

logger = logging.getLogger(__name__)


class UdpProtocol(asyncio.DatagramProtocol):
    transport: DatagramTransport = None

    def connection_made(self, transport: DatagramTransport) -> None:
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('%s:%d - 收到 - %s', *addr, data.hex(' '))
        self.sendto(data, addr)

    def sendto(self, data, addr):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('%s:%d - 发送 - %s', *addr, data.hex(' '))
        self.transport.sendto(data, addr)


async def init_udpserver(config):
    loop = asyncio.get_running_loop()
    logger.info('启动 UDP 服务: {}'.format(config.udp))
    await loop.create_datagram_endpoint(UdpProtocol, local_addr=('0.0.0.0', config.udp))

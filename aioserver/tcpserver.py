import asyncio
import logging
import socket
from asyncio.transports import Transport
from typing import Optional

logger = logging.getLogger(__name__)


class TcpProtocol(asyncio.Protocol):
    peername: str = None
    transport: Transport = None

    def connection_made(self, transport: Transport) -> None:
        self.peername = '{}:{}'.format(*transport.get_extra_info('peername'))
        self.transport = transport

        # 设置 TCP_NODELAY
        sock = transport.get_extra_info('socket')
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        logger.info(f'来自 {self.peername} 的连接已建立')

    def connection_lost(self, exc: Optional[Exception]) -> None:
        logger.info(f'来自 {self.peername} 的连接已断开：{exc or "关闭"}')

    def data_received(self, data: bytes) -> None:
        self.transport.write(data)


async def init_tcpserver(config):
    loop = asyncio.get_running_loop()
    logger.info('启动 TCP 服务: {}'.format(config.tcp))
    await loop.create_server(TcpProtocol, host='0.0.0.0', port=config.tcp)

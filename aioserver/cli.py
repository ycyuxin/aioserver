import asyncio
import json
import logging
import sys
from types import SimpleNamespace

import aiomonitor
import click

from aioserver import __version__
from aioserver.tcpserver import init_tcpserver
from aioserver.udpserver import init_udpserver
from aioserver.web import init_web, run_web

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def init_config(conf_file):
    return SimpleNamespace(**json.load(conf_file))


def init_logger(log_levels):
    logging.basicConfig(format=LOG_FORMAT, level=log_levels.pop('default', 'INFO').upper())

    for name, level in log_levels.items():
        logging.getLogger(name).setLevel(level.upper())


async def on_startup(app):
    config = app['config']
    await init_tcpserver(config)
    await init_udpserver(config)


def start_servers(config):
    web_app = init_web(config)

    web_app.on_startup.append(on_startup)

    with aiomonitor.start_monitor(asyncio.get_event_loop()):
        run_web(web_app)


@click.command()
@click.option('-c', '--conf-file', default='/etc/aioserver.json', type=click.File(encoding='utf-8'), help='配置文件')
@click.option('-d', '--debug', is_flag=True, help='打开调试模式')
def cli(conf_file, debug):
    # 分析配置文件
    config = init_config(conf_file)

    # 初始化日志系统
    init_logger(config.log_levels)

    # 调试模式
    if debug:
        asyncio.get_event_loop().set_debug(debug)

    # 软件版本信息
    logging.info('aioserver-%s' % __version__)

    # Linux 平台上启用 uvloop
    if sys.platform == 'linux':
        import uvloop

        logging.info('uvloop-%s' % uvloop.__version__)
        uvloop.install()

    # 启动服务器
    start_servers(config)


if __name__ == '__main__':
    cli()

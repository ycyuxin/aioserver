import logging
import socket
from pathlib import Path

import aiohttp_debugtoolbar
import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.web_request import BaseRequest
from aiohttp.web_response import StreamResponse

from aioserver import views

logger = logging.getLogger(__name__)


class AccessLogger(web.AbstractAccessLogger):
    def log(self, request: BaseRequest, response: StreamResponse, time: float) -> None:
        self.logger.info(
            f'{request.remote} - {request.method} {request.path} - '
            f'{response.status} - {response.body_length} - {time:.6f}'
        )


def init_web(config):
    app = web.Application()

    app['config'] = config

    # Jinja2 模板
    template_dir = Path(__file__).parent.parent / 'templates'
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(template_dir))

    # 调试工具栏
    aiohttp_debugtoolbar.setup(app, check_host=False)

    app.add_routes([
        web.get('/', views.index_view),
        web.get('/debug', views.debug_view),
        web.post('/debug', views.debug_view),
    ])

    return app


def run_web(app):
    config = app['config']

    logger.info('启动 web 服务: {}'.format(config.web))
    reuse_port = hasattr(socket, 'SO_REUSEPORT')
    web.run_app(app, port=config.web, print=lambda _: None, reuse_port=reuse_port, access_log_class=AccessLogger)

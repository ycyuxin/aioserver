import asyncio
import logging

import aiohttp_jinja2
from aiohttp.web import Request, Response

logger = logging.getLogger(__name__)


async def index_view(_: Request):
    return Response(text='你好!')


@aiohttp_jinja2.template('debug.html')
async def debug_view(request: Request):
    loop = asyncio.get_running_loop()

    if request.method == 'POST':
        data = dict(await request.post())
        action = data.pop('_action')
        if action == 'asyncio':
            debug = data.get('debug', 'off') == 'on'
            loop.set_debug(debug)
        elif action == 'log_level':
            logging.root.setLevel(data.pop('default'))
            for name, level in data.items():
                logging.getLogger(name).setLevel(level)
        else:
            assert False

    # noinspection PyUnresolvedReferences
    loggers = logging.Logger.manager.loggerDict
    loggers = {name: logging.getLevelName(logger_.level)
               for name, logger_ in sorted(loggers.items())
               if not isinstance(logger_, logging.PlaceHolder)}
    return {
        'asyncio': {
            'debug': loop.get_debug(),
        },
        'default': logging.getLevelName(logging.root.level),
        'loggers': loggers,
    }

import asyncio
import logging

from app.core.shared.event_object import EventObject


log = logging.getLogger(__name__)


async def dde(entrypoint, use_cases):
    r, w = await asyncio.open_connection(
        entrypoint.options['listener']['host'],
        entrypoint.options['listener']['port']
    )

    async def auth():
        auth_data = await r.read(1024)
        if 'Login:' in auth_data.decode():
            w.write((entrypoint.options['listener']['auth']['login'] + '\r\n').encode('utf-8'))
            await w.drain()
            auth_data = await r.read(1024)
            if 'Password:' in auth_data.decode():
                w.write((entrypoint.options['listener']['auth']['password'] + '\r\n').encode('utf-8'))
                await w.drain()
                auth_data = await r.readline()
                while 'Access granted' not in auth_data.decode():
                    auth_data = await r.readline()
                return True
        return False

    if await auth():
        log.info('DDE listener started...')
        while True:
            data = await r.read(1024)
            data = data.decode().split('\r\n')
            for q in data:
                q = q.strip().split(' ')
                if len(q) == 3:
                    quote = {
                        'symbol': q[0],
                        'bid': q[1],
                        'ask': q[2],
                        'type': 'quote'
                    }
                    event_obj = EventObject.unpack_event(entrypoint, quote)
                    if event_obj is not None:
                        request_object = event_obj.make_request_object()
                        if not request_object:
                            continue
                        response_object = await use_cases.execute(request_object)

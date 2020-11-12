import json
import logging
import websockets

from asyncio import CancelledError, sleep
from sources.core.shared.event_object import EventObject

log = logging.getLogger(__name__)


async def cryptocompare(entrypoint, use_cases):
    subs = {
        'action': 'SubAdd',
        'subs': entrypoint.options['listener']['subs'],
    }
    while True:
        try:
            async with websockets.connect(entrypoint.options['host'] + entrypoint.options['api_key']) as websocket:
                await websocket.send(json.dumps(subs).encode())
                log.info('Cryptocompare listener started...')
                async for message in websocket:
                    msg = json.loads(message)
                    if int(msg['TYPE']) == 5 and 'FLAGS' in msg and int(msg['FLAGS']) < 3:
                        quote = {
                            'symbol': msg['FROMSYMBOL'] + msg['TOSYMBOL'],
                            'type': 'quote',
                            'ask': msg['PRICE'],
                            'bid': msg['PRICE']
                        }
                        event_obj = EventObject.unpack_event(entrypoint, quote)
                        if event_obj is not None:
                            request_object = event_obj.make_request_object()
                            if not request_object:
                                continue
                            response_object = await use_cases.execute(request_object)
        except CancelledError:
            log.info('Cryptocompare task is canceled...')
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            log.exception(e, exc_info=False)
            await sleep(5)

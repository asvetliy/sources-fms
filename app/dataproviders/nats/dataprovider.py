import logging

from nats.aio.client import Client as NatsClient
from .models import Quote
from .aggregator import Aggregator

log = logging.getLogger(__name__)


class Nats:
    def __init__(self, connection, options_):
        self.options = options_
        self.connection = connection
        if self.options['aggregator']['enabled']:
            self.aggregator = Aggregator(self.connection, self.options['aggregator'])
        else:
            self.aggregator = None

    @classmethod
    async def make(cls, options_):
        nc = NatsClient()

        async def error_cb(e):
            log.warning(str(e))

        async def closed_cb():
            log.warning('Connection to NATS is closed.')

        async def reconnected_cb():
            log.warning(f'Connected to NATS at {nc.connected_url.netloc}...')

        options = {
            'error_cb': error_cb,
            'closed_cb': closed_cb,
            'reconnected_cb': reconnected_cb,
            'servers': options_['servers'],
        }
        await nc.connect(**options)
        return cls(nc, options_)

    async def send_quote(self, quote):
        return self.connection.publish('quotes', quote)

    async def push_quote(self, request_object):
        quote = Quote.make_from_request(request_object)
        if quote.source in self.options['publishers']:
            await self.connection.publish('quotes', str(quote).encode())
        await self.add_quote(quote)
        return '{}'

    async def add_quote(self, quote: Quote):
        if self.aggregator:
            await self.aggregator.current_queue.put(quote)

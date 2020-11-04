import logging

from aiokafka import AIOKafkaProducer
from aiokafka.helpers import create_ssl_context
from .models import Quote
from .aggregator import Aggregator

log = logging.getLogger(__name__)


class Kafka:
    def __init__(self, connection, options_):
        self.options = options_
        self.connection = connection
        if self.options['aggregator']['enabled']:
            self.aggregator = Aggregator(self.connection, self.options['aggregator'])
        else:
            self.aggregator = None

    @classmethod
    async def make(cls, options_, loop):
        context = create_ssl_context(
            cafile=options_['producer']['ssl']['ca'],
            certfile=options_['producer']['ssl']['cert'],
            keyfile=options_['producer']['ssl']['key'],
            password=options_['producer']['ssl']['password'],
        )
        producer = AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=options_['producer']['servers'],
            ssl_context=context,
            security_protocol='SASL_SSL',
            sasl_mechanism=options_['producer']['sasl']['mechanism'],
            sasl_plain_username=options_['producer']['sasl']['username'],
            sasl_plain_password=options_['producer']['sasl']['password'],
        )
        await producer.start()
        return cls(producer, options_)

    async def send_quote(self, quote):
        return await self.connection.send_and_wait(self.options['producer']['topic'], str(quote).encode())

    async def push_quote(self, request_object):
        quote = Quote.make_from_request(request_object)
        if quote.source in self.options['producer']['publishers']:
            await self.send_quote(quote)
        await self.add_quote(quote)
        return '{}'

    async def add_quote(self, quote: Quote):
        if self.aggregator:
            await self.aggregator.current_queue.put(quote)

    async def stop(self):
        return await self.connection.stop()

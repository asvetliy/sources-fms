import asyncio
import logging

from .models import Quote

log = logging.getLogger(__name__)


class Aggregator(object):
    def __init__(self, connection, options):
        self.current_queue = asyncio.Queue()
        self._connection = connection
        self._options = options
        self.agg_table = {}
        self._engine = []
        self._stop = False

        self.loop = asyncio.get_event_loop()
        aggregate_task = self.loop.create_task(self.aggregate(self.current_queue))
        self._engine.append(aggregate_task)

    async def aggregate(self, queue):
        while not self._stop:
            await asyncio.sleep(self._options['agg_time'])
            while not queue.empty():
                q = queue.get_nowait()  # type: Quote
                if q.symbol not in self.agg_table:
                    self.agg_table[q.symbol] = {
                        'bid': 0,
                        'ask': 0,
                        'source': 'aggregator',
                        'symbol': q.symbol,
                        'count': 0
                    }
                if self.agg_table[q.symbol]['count'] == 0:
                    self.agg_table[q.symbol]['bid'] = float(q.bid)
                    self.agg_table[q.symbol]['ask'] = float(q.ask)
                else:
                    self.agg_table[q.symbol]['bid'] += float(q.bid)
                    self.agg_table[q.symbol]['ask'] += float(q.ask)
                self.agg_table[q.symbol]['count'] += 1
            for val in self.agg_table.values():
                if val['count'] > 1:
                    val['bid'] = val['bid'] / val['count']
                    val['ask'] = val['ask'] / val['count']
                quote = Quote('quote', val['symbol'], val['bid'], val['ask'], val['source'])
                await self._connection.publish('quotes', str(quote).encode())
                if val['count'] > 0:
                    val['count'] = 0

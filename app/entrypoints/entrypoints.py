import asyncio
import logging

log = logging.getLogger(__name__)


class Entrypoints:
    def __init__(self, type_, options_):
        self.type = type_
        self.options = options_

    def start(self, use_cases):
        threads = []
        threads_count = self.options.get('threads', None)
        log.info(f'Starting {self.type} entrypoint with {threads_count} threads...')
        if threads_count and self.options.get('enabled', False):
            if self.type == 'cryptocompare':
                from .cryptocompare import cryptocompare
                loop = asyncio.get_event_loop()
                for i in range(0, threads_count):
                    task = loop.create_task(cryptocompare(self, use_cases))
                    threads.append(task)
                return threads
            if self.type == 'dde':
                from .dde import dde
                loop = asyncio.get_event_loop()
                for i in range(0, threads_count):
                    task = loop.create_task(dde(self, use_cases))
                    threads.append(task)
                return threads
            else:
                log.error(f'Unsupported entrypoint type: {self.type}')
                return threads
        else:
            log.warning(f'No threads created for entrypoint type: {self.type}')
            return threads

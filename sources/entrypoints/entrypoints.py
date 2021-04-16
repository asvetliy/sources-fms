import asyncio
import logging

log = logging.getLogger(__name__)


class Entrypoints:
    def __init__(self, type_, options_):
        self.type = type_
        self.options = options_
        self._watcher = None
        self._use_cases = None

    async def watcher(self, threads: list, loop, name):
        while True:
            await asyncio.sleep(5)
            if self._use_cases:
                for t in threads:
                    if t.done() or t.cancelled():
                        log.info(f'Watcher will restart thread of {name} entrypoint...')
                        if name == 'cryptocompare':
                            from .cryptocompare import cryptocompare
                            threads.remove(t)
                            task = loop.create_task(cryptocompare(self, self._use_cases))
                            threads.append(task)
                        if name == 'dde':
                            from .dde import dde
                            threads.remove(t)
                            task = loop.create_task(dde(self, self._use_cases))
                            threads.append(task)

    def start(self, use_cases):
        threads = []
        self._use_cases = use_cases
        if not self.options.get('enabled', False):
            log.warning(f'Disabled entrypoint type: {self.type}. No threads will be created.')
            return threads
        threads_count = self.options.get('threads', None)
        log.info(f'Starting {self.type} entrypoint with {threads_count} thread(s)...')
        if threads_count:
            loop = asyncio.get_event_loop()
            if self.type == 'cryptocompare':
                from .cryptocompare import cryptocompare
                for i in range(0, threads_count):
                    task = loop.create_task(cryptocompare(self, use_cases))
                    threads.append(task)
                    self._watcher = loop.create_task(self.watcher(threads, loop, 'cryptocompare'))
                return threads
            if self.type == 'dde':
                from .dde import dde
                for i in range(0, threads_count):
                    task = loop.create_task(dde(self, use_cases))
                    threads.append(task)
                    self._watcher = loop.create_task(self.watcher(threads, loop, 'dde'))
                return threads
            else:
                log.error(f'Unsupported entrypoint type: {self.type}')
                return threads
        else:
            log.warning(f'No threads created for entrypoint type: {self.type}')
            return threads

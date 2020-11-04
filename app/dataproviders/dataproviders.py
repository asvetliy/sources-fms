class Dataproviders:
    def __init__(self, type_, options_):
        self.type = type_
        self.options = options_

    def make(self):
        if self.type == 'nats':
            from app.dataproviders.nats.dataprovider import Nats
            return Nats.make(self.options)
        if self.type == 'kafka':
            import asyncio
            from app.dataproviders.kafka.dataprovider import Kafka
            loop = asyncio.get_event_loop()
            return Kafka.make(self.options, loop)
        else:
            return None

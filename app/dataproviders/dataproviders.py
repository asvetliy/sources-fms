class Dataproviders:
    def __init__(self, type_, options_):
        self.type = type_
        self.options = options_

    def make(self):
        if self.type == 'nats':
            from app.dataproviders.nats.dataprovider import Nats
            return Nats.make(self.options)
        else:
            return None

from time import time


class Quote(object):
    def __init__(self, type_, symbol_, bid_, ask_, source_):
        self.type = type_
        self.symbol = symbol_
        self.bid = bid_
        self.ask = ask_
        self.source = source_
        self.timestamp = time()

    def __str__(self):
        return f'{{"type": "{self.type}", "symbol": "{self.symbol}",' \
            f' "bid": "{self.bid:.8f}", "ask": "{self.ask:.8f}",' \
            f' "timestamp": "{self.timestamp}", "source": "{self.source}"}}'

    @classmethod
    def make_from_request(cls, request_object):
        if not request_object:
            return None
        type_ = 'quote'
        symbol_ = request_object.data['symbol']
        bid_ = float(request_object.data['bid'])
        ask_ = float(request_object.data['ask'])
        source_ = request_object.type
        if source_.endswith('Quote'):
            source_ = source_[:-5].lower()

        return cls(type_, symbol_, bid_, ask_, source_)

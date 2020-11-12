from sources.core.shared import request_object as req


class CryptocompareQuoteRequestObject(req.ValidRequestObject):
    TYPE = 'CryptocompareQuote'

    def __init__(self, data_):
        super(CryptocompareQuoteRequestObject, self).__init__(self.TYPE, data_)

    @classmethod
    def validate(cls, data=None):
        invalid_req = req.InvalidRequestObject()

        if data is None:
            invalid_req.add_error('request', 'No data in request')
        if invalid_req.has_errors():
            return invalid_req

        return CryptocompareQuoteRequestObject(data)


class DdeQuoteRequestObject(req.ValidRequestObject):
    TYPE = 'DdeQuote'

    def __init__(self, data_):
        super(DdeQuoteRequestObject, self).__init__(self.TYPE, data_)

    @classmethod
    def validate(cls, data=None):
        invalid_req = req.InvalidRequestObject()

        if data is None:
            invalid_req.add_error('request', 'No data in request')
        if invalid_req.has_errors():
            return invalid_req

        return DdeQuoteRequestObject(data)

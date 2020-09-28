from app.core.shared.response_object import ResponseSuccess
from app.core.shared.use_case import UseCase


class CryptocompareQuoteUseCase(UseCase):
    async def process(self, request_object):
        result = await self.repo.push_quote(request_object)
        return ResponseSuccess(result)


class DdeQuoteUseCase(UseCase):
    async def process(self, request_object):
        result = await self.repo.push_quote(request_object)
        return ResponseSuccess(result)

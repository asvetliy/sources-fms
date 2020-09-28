from app.core.shared import response_object as res


class LogTypes:
    TYPE_MESSAGE = 'MESSAGE'
    TYPE_EVENT = 'EVENT'


HTTP_STATUS_CODES = {
    res.ResponseSuccess.SUCCESS: 200,
    res.ResponseFailure.RESOURCE_ERROR: 404,
    res.ResponseFailure.PARAMETERS_ERROR: 400,
    res.ResponseFailure.SYSTEM_ERROR: 500
}

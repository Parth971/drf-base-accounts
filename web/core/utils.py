from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response.data.get('detail'):
        response.data['message'] = response.data.pop('detail')

    # Now add the HTTP status code to the response.
    if response is not None and isinstance(response.data, ReturnDict):
        error = response.data.popitem(last=False)[1]
        response.data = {
            'message': error[0] if len(error) > 0 else error
        }
    return response

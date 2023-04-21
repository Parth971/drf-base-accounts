from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        for k, v in response.data.items():
            response.data[k] = v[0] if isinstance(v, list) and len(v) > 0 else v
    return response

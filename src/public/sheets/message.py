import http


def http_message(data):
    return {
        "statusCode": http.HTTPStatus.OK,
        "Sucess": True,
        "Data": data
    }
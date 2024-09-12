class RequestException(Exception):

    def __init__(self, status_code=500, message=""):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class BadRequestException(RequestException):

    def __init__(self, message=""):
        super().__init__(message=message, status_code=400)


class UnauthorisedAccessException(RequestException):

    def __init__(self, message=""):
        super().__init__(message=message, status_code=403)

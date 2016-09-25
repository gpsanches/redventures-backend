# -*- encoding: utf-8 -*-

class UnreachableServerException(Exception):
    pass


class InvalidRequestException(Exception):
    pass


class InvalidConnection(Exception):
    pass


class InvalidData(Exception):
    pass


class UnexpectedResponse(Exception):
    pass


class ResourceNotFound(Exception):
    pass


class MethodNotImplemented(Exception):
    pass


class SessionException(Exception):
    pass


class NoMoreStepsException(Exception):
    pass

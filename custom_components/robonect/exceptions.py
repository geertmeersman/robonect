"""Exceptions used by Robonect."""


class RobonectException(Exception):
    """Base class for all exceptions raised by Robonect."""

    pass


class RobonectServiceException(Exception):
    """Raised when service is not available."""

    pass


class BadCredentialsException(Exception):
    """Raised when credentials are incorrect."""

    pass


class NotAuthenticatedException(Exception):
    """Raised when session is invalid."""

    pass


class GatewayTimeoutException(RobonectServiceException):
    """Raised when server times out."""

    pass


class BadGatewayException(RobonectServiceException):
    """Raised when server returns Bad Gateway."""

    pass

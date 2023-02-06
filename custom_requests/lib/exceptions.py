#!/usr/bin/env python3

"""Contains custom exceptions with additional functionality."""

import logging
from typing import Callable


class LogException(Exception):
    """Custom exception for logging exceptions before being raised."""

    def __init__(self, message: str, log: Callable = logging.getLogger().error) -> None:
        """Initialize.

        :param message: message to log
        :param log: logger callable
        """
        log(message)
        super().__init__(message)


class UnexpectedStatusCode(LogException):
    """Custom exception for logging and raising an exception when an unexpected status code is returned."""

    def __init__(self, url: str, status_code: int, reason: str, request_text: str) -> None:
        """Initialize.

        :param url: url
        :param status_code: status code
        :param reason: reason for status code
        :param request_text: text response
        """
        message = f"Unexpected status code for '{url}'; received status_code: {status_code}, reason: '{reason}', text: '{request_text}'."
        super().__init__(message)


class UnexpectedRequestResult(LogException):
    """Custom exception for logging and raising an exception when a request has an unexpected result."""

    def __init__(self, status_code: int, reason: str, request_text: str) -> None:
        """Initialize.

        :param status_code: status code
        :param reason: reason for status code
        :param request_text: text response
        """
        message = f"Unexpected request result, received: {status_code} - {reason}\n{request_text}."
        super().__init__(message)


class RateLimitedError(LogException):
    """Custom exception for logging and raising an exception when a request has been rate limited."""

    def __init__(self, url: str, status_code: str, reason: str) -> None:
        """Initialize.

        :param url: url
        :param status_code: status code
        :param reason: reason for status code
        """
        message = f"Experienced rate limiting on '{url}'; received status_code: {status_code}, reason: '{reason}'."
        super().__init__(message, logging.getLogger().debug)

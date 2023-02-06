#!/usr/bin/env python3

"""Contains the logic for interacting with HTTP requests."""

import logging

import requests

from retry_decorator import Retry
from custom_requests.lib.exceptions import UnexpectedStatusCode, UnexpectedRequestResult, RateLimitedError


class Response(object):
    """Responsible for interfacing with a response."""

    def __init__(self, request) -> None:
        """Initialize.

        :param request: request
        """
        self.request = request

    @property
    def url(self) -> dict:
        """Get the url."""
        return self.request.url

    @property
    def headers(self) -> dict:
        """Get the headers."""
        return self.request.headers

    @property
    def status_code(self) -> int:
        """Get the status code."""
        return self.request.status_code

    @property
    def reason(self) -> str:
        """Get the status code reason."""
        return self.request.reason

    @property
    def json(self) -> dict:
        """Get the json results."""
        try:
            return self.request.json()
        except ValueError:
            raise UnexpectedRequestResult(self.status_code, self.reason, self.request.__dict__)

    @property
    def text(self) -> str:
        """Get the text results."""
        return self.request.text

    def __str__(self) -> str:
        """Get results.str()."""
        return self.text


class Request(requests.Session):
    """Responsible for interacting with a request."""

    def __init__(self, logger: logging.LoggerAdapter) -> None:
        """Initialize.

        :param logger: logger
        """
        super().__init__()
        self.logger = logger
        self.base_url = str()
        self.request_headers = dict()
        self.timeout = (10, 15)
        self.allowed_status_codes = (200,)

    def _request(self, method: str, url: str, data: dict, headers: dict, auth: tuple, allow_redirects: bool, timeout: tuple, status_codes: tuple = tuple()) -> Response:
        """Make a request.

        :param url: url
        :param data: data to send
        :param headers: headers to include
        :param auth: http basic authentication username and password
        :param allow_redirects: follow redirects
        :param timeout: connect timeout, read timeout
        :param status_codes: allowed status codes; "*" allows all
        """
        request = getattr(super(), method)(
            url=url,
            data=data or None,
            headers=headers or self.request_headers,
            auth=auth,
            allow_redirects=allow_redirects,
            timeout=timeout or self.timeout
        )
        self.logger.debug(f"HTTP {method.upper()} ({request.status_code}) request '{request.__dict__}'.")
        if request.status_code == 429:
            raise RateLimitedError(request.url, request.status_code, request.reason)
        if request.status_code not in (status_codes or self.allowed_status_codes) and "*" not in status_codes:  # Allow specific status codes
            if request.status_code != 200:
                if request.status_code != 404:  # 404 errors will use the initially declared empty dictionary
                    request.raise_for_status()  # Raise the included non-200 exception for 4xx and 5xx
                raise UnexpectedStatusCode(request.url, request.status_code, request.reason, request.text)
        self.logger.debug(f"Acceptable {method.upper()} status code '{request.status_code}' for '{url}'.")
        return request

    @Retry(jitter=True)
    def get(self, url: str, headers: dict = None, auth: tuple = tuple(), allow_redirects: bool = True, timeout: tuple = tuple(), status_codes: tuple = tuple()) -> Response:
        """Make a GET request.

        :param url: url to get data
        :param headers: headers to include
        :param auth: http basic authentication username and password
        :param allow_redirects: follow redirects
        :param timeout: connect timeout, read timeout
        :param status_codes: allowed status codes; "*" allows all
        """
        self.logger.debug(f"Making a GET request to '{url}' with the headers '{headers}' and auth '{auth}'.")
        return Response(
            self._request(
                method="get",
                url=url,
                data=dict(),
                headers=headers or dict(),
                auth=auth,
                allow_redirects=allow_redirects,
                timeout=timeout,
                status_codes=status_codes
            )
        )

    @Retry(jitter=True)
    def post(self, url: str, data: dict = None, headers: dict = None, auth: tuple = tuple(), allow_redirects: bool = True, timeout: tuple = tuple(), status_codes: tuple = tuple()) -> Response:
        """Make a POST request.

        :param url: url to post data
        :param data: data to post
        :param headers: headers to include
        :param auth: http basic authentication username and password
        :param allow_redirects: follow redirects
        :param timeout: connect timeout, read timeout
        :param status_codes: allowed status codes; "*" allows all
        """
        self.logger.debug(f"Making a POST request to '{url}' with the data '{data}' and headers '{headers}'.")
        return Response(
            self._request(
                method="post",
                url=url,
                data=data or dict(),
                headers=headers or dict(),
                auth=auth,
                allow_redirects=allow_redirects,
                timeout=timeout,
                status_codes=status_codes
            )
        )

    @Retry(jitter=True)
    def head(self, url: str, headers: dict = None, auth: tuple = tuple(), allow_redirects: bool = False, timeout: tuple = tuple(), status_codes: tuple = tuple()) -> Response:
        """Make a HEAD request.

        :param url: url to get header data
        :param headers: headers to include
        :param auth: http basic authentication username and password
        :param allow_redirects: follow redirects
        :param timeout: connect timeout, read timeout
        :param status_codes: allowed status codes; "*" allows all
        """
        self.logger.debug(f"Making a HEAD request to '{url}' with the headers '{headers}' and auth '{auth}'.")
        return Response(
            self._request(
                method="head",
                url=url,
                data=dict(),
                headers=headers or dict(),
                auth=auth,
                allow_redirects=allow_redirects,
                timeout=timeout,
                status_codes=status_codes
            )
        )

    @Retry(jitter=True)
    def patch(self, url: str, data: dict = None, headers: dict = None, auth: tuple = tuple(), allow_redirects: bool = True, timeout: tuple = tuple(), status_codes: tuple = tuple()) -> Response:
        """Make a PATCH request.

        :param url: url to patch data
        :param data: data to patch
        :param headers: headers to include
        :param auth: http basic authentication username and password
        :param allow_redirects: follow redirects
        :param timeout: connect timeout, read timeout
        :param status_codes: allowed status codes; "*" allows all
        """
        self.logger.debug(f"Making a PATCH request to '{url}' with the headers '{headers}' and auth '{auth}'.")
        return Response(
            self._request(
                method="patch",
                url=url,
                data=data or dict(),
                headers=headers or dict(),
                auth=auth,
                allow_redirects=allow_redirects,
                timeout=timeout,
                status_codes=status_codes
            )
        )

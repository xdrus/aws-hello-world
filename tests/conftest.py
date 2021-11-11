"""Shared fictures and tests configuration."""

import pytest
import urllib.request
import urllib.error


def pytest_addoption(parser):
    """Add options to configure tests behaiviour."""
    parser.addoption("--url", action="store", help="URL to check")


@pytest.fixture(scope="module")
def url(request):
    """
    Return URL specified in command line.

      * if `--url` parameter is set use it
      * raise error if url is not set
    """
    if request.config.option.url:
        return request.config.option.url

    raise ValueError(
        "Please provide URL in format https://site-domain/site-path to test"
    )


@pytest.fixture(scope="module")
def response(url):
    """
    Return response object for URL to validate site work.

    This fixture allows to reuse one connection per module to speed up tests.
    """

    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        return e


@pytest.fixture(scope="module")
def response_content(response):
    """
    Return response content (i.e. html).

    This fixture allows to get content once per module to speed up tests.
    """

    return response.read()

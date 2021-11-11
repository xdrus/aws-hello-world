"""Test permissions of the site to ensure we haven't given write access."""

import pytest
import urllib.request
import urllib.error


@pytest.mark.parametrize("method", ["PUT", "POST"])
def test_write_is_not_allowed(url, method):
    """Test that WRITE methods are not allowed."""
    req = urllib.request.Request(url, data=b"", method=method)
    with pytest.raises(expected_exception=urllib.error.HTTPError) as excinfo:
        response = urllib.request.urlopen(req)
    assert excinfo.value.code == 403

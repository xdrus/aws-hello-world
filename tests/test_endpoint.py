"""Run test against endpoint."""


def test_return_200(response):
    """Test that URL returns 200."""
    assert response.status == 200


def test_return_html(response):
    """Test that response type is html."""
    assert "html" in str(response.headers["Content-Type"])


def test_return_expected_content(response_content):
    """Test that URL returns a page with 'hello world' message."""
    assert "hello world" in str(response_content)

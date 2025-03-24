import pytest

from zimitfrontend.utils import normalize_hostname


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://EXAMPLE.com/path",
            "https://example.com/path",
        ),
        (
            "http://www.test.EXAMPLE.com/pAth",
            "http://www.test.example.com/pAth",
        ),
        (
            "eXamPle.com/Path",
            "example.com/Path",
        ),
        (
            "https://TesT.EXAMPLE.com/PATH",
            "https://test.example.com/PATH",
        ),
        (
            "http://www.exAmPLE.com/p1/P2/p?q=k&O=x#Fr",
            "http://www.example.com/p1/P2/p?q=k&O=x#Fr",
        ),
        (
            "www.example.com/Path/path2?Q=a#fragment",
            "www.example.com/Path/path2?Q=a#fragment",
        ),
    ],
)
def test_lower_case_url_hostname(url: str, expected: str):
    assert normalize_hostname(url) == expected

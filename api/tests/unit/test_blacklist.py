from re import compile

import pytest

from zimitfrontend.blacklist import BlacklistedUrl, UrlBlacklistManager

manager = UrlBlacklistManager()
manager.blacklist.append(
    BlacklistedUrl(
        reason_key="blacklist.not_working",
        url_regex=compile(r"^https?:\/\/www\.acme\.com(?:\/.*)?$"),
    )
)
manager.blacklist.append(
    BlacklistedUrl(
        reason_key="blacklist.already_done",
        url_regex=compile(r"^https?:\/\/en\.wikipedia\.org(?:\/.*)?$"),
    )
)


@pytest.mark.parametrize(
    "url,expected",
    [
        pytest.param("http://www.acme.com", "blacklist.not_working"),
        pytest.param("https://www.acme.com", "blacklist.not_working"),
        pytest.param("https://www.acme.com/foo", "blacklist.not_working"),
        pytest.param("https://en.wikipedia.org", "blacklist.already_done"),
        pytest.param("https://en.wikipedia.org/wiki/Foo", "blacklist.already_done"),
        pytest.param("https://www.foo.com", None),
        pytest.param("https://www.foo.com?href=http://www.acme.com", None),
    ],
)
def test_blacklist(url: str, expected: str | None):
    assert manager.get_blacklist_reason(url) == expected

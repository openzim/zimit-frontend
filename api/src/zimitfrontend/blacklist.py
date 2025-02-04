import csv
import dataclasses
from http import HTTPStatus
from re import Pattern, compile

import requests

from zimitfrontend.constants import ApiConfiguration, logger


@dataclasses.dataclass(kw_only=True)
class BlacklistedUrl:
    reason_key: str
    url_regex: Pattern[str]


class UrlBlacklistManager:

    def __init__(self):
        self.blacklist: list[BlacklistedUrl] = []

    def get_blacklist_reason(self, url: str) -> str | None:
        """Return the blacklist reason key or None

        If url passed is blacklisted, then this function returns the blacklist reason,
        otherwise None is returned
        """

        def _is_match(url: str, blacklist_item: BlacklistedUrl) -> bool:
            return blacklist_item.url_regex.match(url) is not None

        matching = list(filter(lambda item: _is_match(url, item), self.blacklist))

        return matching[0].reason_key if matching else None

    def load_from_url(self, url: str) -> None:
        resp = requests.get(
            url, allow_redirects=True, timeout=ApiConfiguration.other_requests_timeout
        )
        if not HTTPStatus(resp.status_code).is_success:
            logger.warning(
                f"Error fetching blacklist from {url}: {resp.status_code} "
                f"({resp.content.decode()[:1024] if resp.content else 'no body'})"
            )
        if not resp.content:
            logger.warning(f"Empty content in blacklist at {url}: {resp.status_code}")
        csvreader = csv.DictReader(
            resp.content.decode().splitlines(), ["url_regex", "reason_key"]
        )
        new_blacklist: list[BlacklistedUrl] = []
        for row in csvreader:
            new_blacklist.append(
                BlacklistedUrl(
                    reason_key=row["reason_key"],
                    url_regex=compile(row["url_regex"]),
                )
            )
        logger.info(f"{len(new_blacklist)} urls have been loaded into blacklist")
        self.blacklist = new_blacklist


blacklist_manager = UrlBlacklistManager()


def refresh_blacklist():
    if not ApiConfiguration.blacklist_url:
        return
    blacklist_manager.load_from_url(ApiConfiguration.blacklist_url)

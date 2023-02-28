"""
Combines IPs from data exports which include IP addresses
"""

REQUIRES = ["git+https://github.com/seanbreckenridge/ipgeocache"]

from typing import Iterator

from my.ip.common import IP  # type: ignore[import]
from my.core.common import LazyLogger, Stats
from my.core.denylist import DenyList

logger = LazyLogger(__name__)


# helper to get path to data file in my data directory
from my.utils.backup_to.__main__ import get_dir as hpi_data_file

denydir = hpi_data_file("denylist")
deny = DenyList(denydir / "ips.json")


def _ips() -> Iterator[IP]:
    # can add more sources here, or disable them through core.disabled_modules
    from my.ip import facebook, discord, blizzard

    yield from facebook.ips()
    yield from discord.ips()
    yield from blizzard.ips()

def ips() -> Iterator[IP]:
    yield from deny.filter(_ips())


def stats() -> Stats:
    from my.core import stat

    return {**stat(ips)}
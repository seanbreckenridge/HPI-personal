"""
Merges location data from multiple sources -- this includes apple location data as well
"""

from typing import Iterator

from my.core import Stats, make_logger

from my.location import apple  # additional source
from my.location import google_takeout, gpslogger, google_takeout_semantic
from my.core.error import warn_exceptions

from my.location.common import Location


logger = make_logger(__name__, level="warning")


def locations() -> Iterator[Location]:
    yield from warn_exceptions(google_takeout_semantic.locations())
    yield from google_takeout.locations()
    yield from gpslogger.locations()
    yield from apple.locations()


def stats() -> Stats:
    from my.core import stat

    return {
        **stat(locations),
    }

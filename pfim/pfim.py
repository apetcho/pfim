"""PFIM: Personal Finance Manager"""

from collections import namedtuple
from email.generator import Generator
from email.mime import audio
from enum import Enum, auto

from platformdirs import sys
from _version import __PFIM_VERSION

# Global Constants and Structures
PfimEntry = namedtuple("PfimEntry", "date tag kind amount")
PFIM_VERSION = __PFIM_VERSION
del __PFIM_VERSION
_DBNAME = "pfimdata.db"
_EARN_KIND = "E"
_SPENT_KIND = "S"

# --- PFIM utility class --


class OutputBeautify:
    class Color(Enum):
        pass

    class Format(Enum):
        pass

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


class PfimData:
    """PFIM database interface."""

    def __init__(self):
        pass

    def start_session(self, *args) -> None:
        pass

    def close_session(self, *args) -> None:
        pass

    def add_entry(self, entry: PfimEntry) -> None:
        pass

    def fetch(self, query: str) -> Generator:
        pass

    def update(self, query: str) -> None:
        pass

    def delete(self, query: str) -> None:
        pass



class PfimCore:
    """PFIM Core class."""
    class InteractivePfimCmds:
        def __init__(self):
            pass

        def add(self, **kwargs):
            pass

        def report(self, **kwargs):
            pass

        def summary(self, **kwargs):
            pass

        def quit(self):
            pass

    class QueryType(Enum):
        ADD = auto()
        FETCH = auto()
        UPDATE = auto()
        DELETE = auto()

    class Report:
        pass

    class ReportSummary:
        pass

    prolog = ""
    epilog = ""
    Output = namedtuple("Output", "report summary")
    QueryKey = namedtuple("QueryKey", "key type")

    def __init__(self):
        self._version = PFIM_VERSION
        self._queries_map = {}
        self._mode = None
        self._output = None

    def _init_queries_map(self):
        pass

    def _set_query(self, key: QueryKey) -> None:
        pass

    def _get_query(self, key: QueryKey) -> str:
        pass

    def make_output(self) -> Output:
        pass

    def write_output(self, file=sys.stdout):
        pass

    @staticmethod
    def cmd_parser():
        pass


def main():
    pass

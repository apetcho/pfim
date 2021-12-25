"""PFIM: Personal Finance Manager"""

import os
import sys

from enum import Enum
from collections import namedtuple
from _version import __PFIM_VERSION
from typing import List, Dict, Callable, Generator, Mapping


# Global Constants and Structures
PfimEntry = namedtuple("PfimEntry", "date tag kind amount")
Output = namedtuple("Output", "report summary")
QueryKey = namedtuple("QueryKey", "key type")
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
        # start the db: create a new if it doesn't exists
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


class InteractivePfim:
    PROMPT = "pfim>> "

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


class Report:
    pass

class ReportSummary:
    pass


class PfimCore:
    """PFIM Core class."""
    
    prolog = ""
    epilog = ""
    ADD = 1
    FETCH = 2
    UPDATE = 3
    DELETE = 4

    def __init__(self):
        self._version = PFIM_VERSION
        self._query_map = {}
        self._mode = None
        self._output = None

    def _init_query_map(self):
        """Initial query map"""
        ADD = PfimCore.QueryKey.ADD
    
        self._query_map[(PfimCore.QueryType)]

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

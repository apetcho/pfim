"""PFIM: Personal Finance Manager"""

import os
import sys
import sqlite3
import logging
import argparse
from datetime import date, timedelta
from enum import Enum
from collections import namedtuple
from _version import __PFIM_VERSION
from typing import List, Dict, Callable, Generator, Mapping

## -- set up a logger for the application
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
_filehandler = logging.FileHandler(
    os.path.join(os.environ["HOMe"], ".pfim.log"))
_filehandler.setLevel(logging.DEBUG)
_consolehandler = logging.StreamHandler()
_consolehandler.setLevel(logging.ERROR)
_formatter = logging.Formatter(
    "[%(asctime)s]::%(name)s::%(message)s")
_filehandler.setFormatter(_formatter)
_consolehandler.setFormatter(_formatter)


# Global Constants and Structures
PfimEntry = namedtuple("PfimEntry", "date tag kind amount")
Output = namedtuple("Output", "report summary")
# QueryKey = namedtuple("QueryKey", "key")
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
        self._logger = logging.getLogger("pfim.PfimData")
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
        self._logger = logging.getLogger("pfim.InteractivePfim")
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
    def __init__(self):
        self._logger = logging.getLogger("pfim.Report")

class ReportSummary:
    def __init__(self):
        self._logger = logging.getLogger("pfim.ReportSummary")


class PfimCore:
    """PFIM Core class."""
    
    prolog = ""
    epilog = ""
    ADD = 1
    FETCH = 2
    UPDATE = 3
    DELETE = 4

    def __init__(self):
        self._logger = logging.getLogger("pfim.PfimCore")
        self._version = PFIM_VERSION
        self._query_map:Mapping[tuple, Callable] = {}
        self._mode = None
        self._output = None

    def _init_query_map(self) -> None:
        """Initial query map"""
        ADD = PfimCore.ADD
        FETCH = PfimCore.FETCH
        DELETE = PfimCore.DELETE
        UPDATE = PfimCore.UPDATE
        # -- add entry
        keyfn = lambda *args : {item for item in args}
        # entry = (earned | spent) + [tag]
        self._query_map[(ADD, keyfn("spent"))] = None
        self._query_map[(ADD, keyfn("earned"))] = None
        self._query_map[(ADD, keyfn("spent", "tag"))] = None
        self._query_map[(ADD, keyfn("earned", "tag"))] = None
        
        # -- Fetch Operations
        # 1. fetch_tag([(,)|(date)|(date+kind)|(kind)])
        self._query_map[(FETCH, keyfn("tag"))] = None
        self._query_map[(FETCH, keyfn("tag", "date"))] = None
        self._query_map[(FETCH, keyfn("tag", "kind"))] = None
        self._query_map[(FETCH, keyfn("tag", "kind", "date"))] = None
        # 2. fetch_kind([(,)|(date)|(date+kind)|(tag)])
        self._query_map[(FETCH, keyfn("kind"))] = None
        self._query_map[(FETCH, keyfn("kind", "tag"))] = None
        self._query_map[(FETCH, keyfn("kind", "date"))] = None
        self._query_map[(FETCH, keyfn("kind", "date", "tag"))] = None
        # 3. fetch_date([(,)|(tag)|(tag+kind)|(kind)])
        self._query_map[(FETCH, keyfn("date"))] = None
        self._query_map[(FETCH, keyfn("date", "tag"))] = None
        self._query_map[(FETCH, keyfn("date", "kind"))] = None
        self._query_map[(FETCH, keyfn("date", "tag", "kind"))] = None
        # 4. fetch_all()
        self._query_map[(FETCH, keyfn("fetch"))] = None
        # -- Update Operations
        self._query_map[(UPDATE, keyfn("update"))] = None
        # -- Delete Operations
        self._query_map[(DELETE, keyfn("delete"))] = None


    def _set_query(self, key: set) -> None:
        pass

    def _get_query(self, key: set) -> str:
        pass

    def make_output(self) -> Output:
        pass

    def write_output(self, file=sys.stdout):
        pass

    @staticmethod
    def cmd_parser():
        _logger = logging.getLogger("pfim.PfimCore.cmd_parser")
        pass


def main():
    pass


del _filehandler, _consolehandler, _formatter

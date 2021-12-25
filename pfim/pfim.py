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
    os.path.join(os.environ["HOME"], ".pfim.log"))
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
_DBNAME = os.path.join(os.environ["HOME"], ".pfimdata.db")
_EARN_KIND = "E"
_SPENT_KIND = "S"


# --- PFIM utility class --


class OutputBeautify:
    class Color(Enum):
        pass

    class Format(Enum):
        pass

    def __init__(self):
        self._logger = logging.getLogger("pfim.Pfim.OutPutBeautify")
        pass

    def __call__(self, *args, **kwargs):
        pass


def _adapter(dateObj: date):
    return dateObj.isoformat()


def _converter(datestr: str):
    return date.fromisoformat(datestr)

sqlite3.register_adapter(date, _adapter)
sqlite3.register_converter("date", _converter)

class PfimData:
    """PFIM database interface."""

    def __init__(self):
        self._logger = logging.getLogger("pfim.PfimData")
        # start the db: create a new if it doesn't exists
        sql = """CREATE TABLE IF NOT EXISTS pfim(
            id INTEGER PRIMARY KEY AUTOINCREMENT NON NULL,
            opdate DATE,
            tag TEXT,
            kind TEXT,
            amount REAL
        )"""
        with sqlite3.connect(_DBNAME,
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
            ) as conn:
            conn.cursor().execute(sql).commit()

    def add_entry(self, entry: PfimEntry) -> None:
        pass

    def fetch(self, query: str) -> Generator:
        pass

    def update(self, query: str) -> None:
        pass

    def delete(self, query: str) -> None:
        pass


class InteractivePfim:
    # Use builtin module *Cmd* ?
    PROMPT = "pfim>> "

    def __init__(self):
        self._logger = logging.getLogger("pfim.InteractivePfim")
        pass

    def add(self, **kwargs):
        pass

    def show(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def update(self, **args):
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
        self._current_query = None

    def _init_query_map(self) -> None:
        """Initial query map"""
        ADD = PfimCore.ADD
        FETCH = PfimCore.FETCH
        DELETE = PfimCore.DELETE
        UPDATE = PfimCore.UPDATE
        self._query_map = dict()   # Make sure this is completely new @start

        """
        # group1
        1. pfim --earned --amount=VALUE
        2. pfim --earned --tag=TAG --amount=VALUE
        3. pfim --earned --date=YYYY-MM-DD --amount=VALUE
        4. pfim --earned --tag=TAG --date=YYYY-MM-DD --amount=VALUE
        # group2
        5. pfim --spent --amount=VALUE
        6. pfim --spent --tag=TAG --amount=VALUE
        7. pfim --spent --date=YYYY-MM-DD --amount=VALUE
        8. pfim --spent --tag=TAG --date=YYYY-MM-DD --amount=VALUE
        # group3
        9. pfim --show
        10. pfim --show --sort-date
        11. pfim --show --sort-tag
        12. pfim --show --sort-amount
        13. pfim --show --before-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
        14. pfim --show --after-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
        # group4
        15. pfim --show-earned
        16. pfim --show-earned --sort-date
        17. pfim --show-earned --sort-tag
        18. pfim --show-earned --sort-amount
        19. pfim --show-earned --before-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
        20. pfim --show-earned --after-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
        # group5
        21. pfim --show-spent
        22. pfim --show-spent --sort-date
        23. pfim --show-spent --sort-tag
        24. pfim --show-spent --sort-amount
        24. pfim --show-spent --before-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
        25. pfim --show-spent --after-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
        # group6
        26. pfim --update --tag=TAG1 --new-tag=TAG2
        27. pfim --update --date=YYYY-MM-DD
        28. pfim --update --earned --amount=VALUE1 --new-amount=VALUE2
        29. pfim --update --spent --amount=VALUE2 --new-amount=VALUE2
        # group7
        30. pfim --delete-all
        31. pfim --delete --tag=TAG1
        32. pfim --delete --date=YYYY-MM-DD
        33. pfim --delete --earned --amount=VALUE
        34. pfim --deltte --spent --amount=VALUE

        """
        # -- add entry
        keyfn = lambda query, *args : ({item for item in args}, query)
        # entry = (earned | spent) + [tag]
        query = None
        self._query_map[(ADD, keyfn(query, "spent"))] = None
        self._query_map[(ADD, keyfn(query, "earned"))] = None
        self._query_map[(ADD, keyfn(query, "spent", "tag"))] = None
        self._query_map[(ADD, keyfn(query, "earned", "tag", ))] = None
        # -- Fetch Operations
        # 1. fetch_tag([(,)|(date)|(date+kind)|(kind)])
        self._query_map[(FETCH, keyfn(query, "tag"))] = None
        self._query_map[(FETCH, keyfn(query, "tag", "date"))] = None
        self._query_map[(FETCH, keyfn(query, "tag", "kind"))] = None
        self._query_map[(FETCH, keyfn(query, "tag", "kind", "date"))] = None
        # 2. fetch_kind([(,)|(date)|(date+kind)|(tag)])
        self._query_map[(FETCH, keyfn(query, "kind"))] = None
        self._query_map[(FETCH, keyfn(query, "kind", "tag"))] = None
        self._query_map[(FETCH, keyfn(query, "kind", "date"))] = None
        self._query_map[(FETCH, keyfn(query, "kind", "date", "tag"))] = None
        # 3. fetch_date([(,)|(tag)|(tag+kind)|(kind)])
        self._query_map[(FETCH, keyfn(query, "date"))] = None
        self._query_map[(FETCH, keyfn(query, "date", "tag"))] = None
        self._query_map[(FETCH, keyfn(query, "date", "kind"))] = None
        self._query_map[(FETCH, keyfn(query, "date", "tag", "kind"))] = None
        # 4. fetch_all()
        self._query_map[(FETCH, keyfn(query,"fetch"))] = None
        # -- Update Operations
        self._query_map[(UPDATE, keyfn(query, "update"))] = None
        # -- Delete Operations
        self._query_map[(DELETE, keyfn(query, "delete"))] = None


    def _set_query(self, key: set) -> None:
        pass

    def _get_query(self, key: set) -> str:
        pass

    def make_output(self) -> Output:
        pass

    def write_output(self, file=sys.stdout):
        pass

    def create_entry(self, *args, **kw):
        pass

    def create_query(self, *arg, **kw):
        pass

    @staticmethod
    def cmd_parser():
        _logger = logging.getLogger("pfim.PfimCore.cmd_parser")
        VERSION = PFIM_VERSION
        USAGE = """
        pfim [-h | --help]
        pfim [-v | --version]
        
        pfim --interactive

        pfim --earned --amount=VALUE
        pfim --earned --tag=TAG --amount=VALUE
        pfim --earned --date=YYYY-MM-DD --amount=VALUE
        pfim --earned --tag=TAG --date=YYYY-MM-DD --amount=VALUE

        pfim --spent --amount=VALUE
        pfim --spent --tag=TAG --amount=VALUE
        pfim --spent --date=YYYY-MM-DD --amount=VALUE
        pfim --spent --tag=TAG --date=YYYY-MM-DD --amount=VALUE
        
        pfim --show
        pfim --show --sort-date
        pfim --show --sort-tag
        pfim --show --sort-amount
        pfim --show --before-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
        pfim --show --after-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]

        pfim --show-earned
        pfim --show-earned --sort-date
        pfim --show-earned --sort-tag
        pfim --show-earned --sort-amount
        pfim --show-earned --before-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
        pfim --show-earned --after-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]

        pfim --show-spent
        pfim --show-spent --sort-date
        pfim --show-spent --sort-tag
        pfim --show-spent --sort-amount
        pfim --show-spent --before-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
        pfim --show-spent --after-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]

        pfim --update --tag=TAG1 --new-tag=TAG2
        pfim --update --date=YYYY-MM-DD
        pfim --update --earned --amount=VALUE1 --new-amount=VALUE2
        pfim --update --spent --amount=VALUE2 --new-amount=VALUE2

        pfim --delete-all
        pfim --delete --tag=TAG1
        pfim --delete --date=YYYY-MM-DD
        pfim --delete --earned --amount=VALUE
        pfim --deltte --spent --amount=VALUE
        """
        parser = argparse.ArgumentParser(
            prog="pfim",
            usage=USAGE,
            description="PFIM: Personal Finance Manager",
            epilog=""
        )

        # group1
        # group2
        # group3
        # group4
        # group5
        # group6
        # group7

        return parser


def main():
    parser = PfimCore.cmd_parser()
    parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()


del _filehandler, _consolehandler, _formatter


if __name__ == "__main__":
    main()

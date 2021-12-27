"""PFIM: Personal Finance Manager"""

from ast import For
import os
from queue import Queue
import sys
import sqlite3
import logging
import statistics
import functools
from datetime import date, timedelta
from enum import Enum, auto
from collections import namedtuple
from tkinter.tix import Form
from tkinter.ttk import Style

from typing import List, Dict, Callable, Generator, Mapping, Union

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
PfimEntry = namedtuple("PfimEntry", "date tag description amount")
Output = namedtuple("Output", "report summary")
QueryOperation = namedtuple("QueryOperation", "query operation args")

_DBNAME = os.path.join(os.environ["HOME"], ".pfimdata.db")
_EARN_KIND = "E"
_SPENT_KIND = "S"

# ---- DATABASE OPERATION CONSTANT ----
RECORD = 1
FETCH = 2
UPDATE = 3
DELETE = 4

_PFIMCmdDoc = {}

def _register_cmd_doc(func):
    functools.wraps(func)
    def wrapper(*args, **kws):
        fname = func.__name__
        fname = fname[1:] if fname.startswith("_") else fname
        # fname = fname[:len(fname)-4] if fname[-4:] == "_doc" else fname
        _PFIMCmdDoc[fname] = func.__doc__
        return
    return wrapper
#-record-rcv, -record-xpx, -show, -show-rcv, -show-xpx, -update,
#-update-rcv, -update-xpx, -delete, -delete-rcv, -delete-xpx
@_register_cmd_doc
def _record_rcv():
    """record_rcv()
    Record an income entry into PFIM backend database.
    
    This command requires information supplied through its options.
    The option are as follow.
    
    Options:
    --tag           Tag given to this entry. The tag option can be ignored. If
                    ignored, the field will simply be filled with a default 
                    symbol "N/A", meaning Not Available.
    --date          This is the date on which the supposed entry was actually 
                    made. The date option can be ignored, in which the current 
                    date is considered.
    --descr         A short description for the entry. It must not exceed 30
                    ASCII characters, otherwise it will be truncated.
    --amount        The value of the income being entered into the database.
                    
    Example
    ------- 
    In pfim default mode:
     
    $ pfim --date=2021-12-26 --descr="Payment from M. Eric" --tag=PWM \
        --amount=275.00

    In interactive mode:
    
    $ pfim --interactive
    pfim>> record_rcv --date=2021-12 --descr="Payment from M. Eric" --tag=PWM \
        --amount=275.00 
    """
    pass
_record_rcv()


@_register_cmd_doc
def _record_xpx():
    """record_xpx()
    Record an expense entry into PFIM backend database.
    
    This command requires information supplied through its options.
    The option are as follow.
    
    Options:
    --tag           Tag given to this entry. The tag option can be ignored. If
                    ignored, the field will simply be filled with a default 
                    symbol "N/A", meaning Not Available.
    --date          This is the date on which the supposed entry was actually 
                    made. The date option can be ignored, in which the current 
                    date is considered.
    --descr         A short description for the entry. It must not exceed 30
                    ASCII characters, otherwise it will be truncated.
    --amount        The value of the expense being entered into the database.
                                     
    Example
    ------- 
    In pfim default mode:
     
    $ pfim --date=2021-12-26 --descr="Bought Cinema ticket" --tag=OUT  \
        --amount=75.00

    In interactive mode:
    
    $ pfim --interactive
    pfim>> record_rcv --date=2021-12 --descr="Bout Ciema ticket" --tag=OUT \
        --amount=275.00 
    """
    pass

@_register_cmd_doc
def _show():
    """show()
    """
    pass

@_register_cmd_doc
def _show_xpx():
    """show_xpx()
    """
    pass

@_register_cmd_doc
def _show_rcv():
    """show_rcv()
    """
    pass


@_register_cmd_doc
def _update():
    """update()
    """
    pass

@_register_cmd_doc
def _update_xpx():
    """update_xpx()
    """
    pass


@_register_cmd_doc
def _update_rcv():
    """update_rcv()
    """
    pass


@_register_cmd_doc
def _delete():
    """delete()
    """
    pass


@_register_cmd_doc
def _delete_xpx():
    """delete_xpx()
    """
    pass

@_register_cmd_doc
def _delete_rcv():
    """delete_rcv()
    """
    pass


# --- PFIM utility class --


class OutputBeautify:

    def __init__(self, textstr: str):
        #self._logger = logging.getLogger("pfim.Pfim.OutPutBeautify")
        self._textstr = textstr

    def decorate(self, color="green", slant="normal", underline=False,
        bold=False):
        mapping = {
            "black": 30, "red": 31, "green": 32, "yellow": 33,
            "blue": 34, "magenta": 35, "cyan": 36, "white": 37,
        }
        stylemap = {"noraml": 0, "bold": 1, "italic": 3, "underline": 4}
        base = 38
        if color.lower() in mapping.keys():
            cval = mapping[color.lower()]
        else:
            cval = mapping["black"]
        txt = self._textstr
        if slant.lower() in ("italic", "normal"):
            sval = stylemap[slant.lower()]
        else:
            sval = stylemap["normal"]
        uval = stylemap["underline"] if underline else None
        bval = stylemap["bold"] if bold else None

        deco = f"\x1b[{base};" #"\x1b[m"
        if sval:
            deco = deco + f"{sval};"
        if uval:
            deco = deco + f"{uval};"
        if bval:
            deco = deco + f"{bval};"

        deco = deco + f"{cval}m;{txt}\x1b[m"
        return deco


def _adapter(dateObj: date):
    return dateObj.isoformat()


def _converter(datestr: str):
    return date.fromisoformat(datestr)

sqlite3.register_adapter(date, _adapter)
sqlite3.register_converter("date", _converter)

class PfimQueryCmdEnum(Enum):
    RECORD_RCV = auto()
    RECORD_XPX = auto()
    SHOW = auto()
    SHOW_RCV = auto()
    SHOW_XPX = auto()
    UPDATE = auto()
    # UPDATE_DESC = auto()  # FIXME: maybe included as a new command
    UPDATE_RCV = auto()
    UPDATE_XPX = auto()
    DELETE = auto()
    DELETE_RCV = auto()
    DELETE_XPX = auto()


def _validate_datestr(datestr: str) -> bool:
    result = None
    try:
        result = date.fromisoformat(datestr)
    except Exception:
        result = None
    if result is None:
        return False
    return True


class PfimData:
    """PFIM database interface."""

    def __init__(self):
        self._logger = logging.getLogger("pfim.PfimData")
        # start the db: create a new if it doesn't exists
        sql = """CREATE TABLE IF NOT EXISTS pfim(
            id INTEGER PRIMARY KEY AUTOINCREMENT NON NULL,
            opdate DATE,
            tag TEXT,
            description TEXT,
            amount REAL
        )"""
        with sqlite3.connect(_DBNAME,
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
            ) as conn:
            conn.cursor().execute(sql).commit()

    def _run_query(self, query, *args, out=False) ->Union[sqlite3.Cursor, None]:
        retval = None
        with sqlite3.connect(_DBNAME) as conn:
            if args:
                retval = conn.cursor().execute(query, args)
            else:
                retval = conn.cursor().execute(query)

            conn.commit()
        if out:
            return retval

    def add_entry(self, query: str, *args) -> None:
        try:
            self._run_query(query, args)
            self._logger.debug("New entry added")
        except sqlite3.Error as err:
            self._logger.error(f"Failed to add a new entry to database. {err}")
            sys.exit(1)

    def fetch(self, query: str, *args) -> Generator:
        try:
            retval = self._run_query(query, args)
            self._logger.debug("Fetched data from database")
        except sqlite3.Error as err:
            self._logger.error(f"Failed to fetch data from database. {err}")
            sys.exit(1)

        for row in retval:
            yield row

    def update(self, query: str, *args) -> None:
        try:
            retval = self._run_query(query, args)
            self._logger.debug("Updated database content")
        except sqlite3.Error as err:
            self._logger.error(f"Failed to update database content. {err}")
            sys.exit(1)

        for row in retval:
            yield row

    def delete(self, query: str, *args) -> None:
        try:
            retval = self._run_query(query, args)
            self._logger.debug("Deleted data from database")
        except sqlite3.Error as err:
            self._logger.error(f"Failed to delete data from database. {err}")
            sys.exit(1)

        for row in retval:
            yield row


class InteractivePfim:
    # Use builtin module *Cmd* ?
    PROMPT = "pfim>> "

    def __init__(self):
        self._logger = logging.getLogger("pfim.InteractivePfim")
        pass

    def record_rcv(self, kw: Dict) -> QueryOperation:
        pass

    def record_xpx(self, kw: Dict) -> QueryOperation:
        pass

    def show(self, kw: Dict) -> QueryOperation:
        pass

    def show_rcv(self, kw: Dict) -> QueryOperation:
        pass

    def show_xpx(self, kw: Dict) -> QueryOperation:
        pass

    def delete(self, kw: Dict) -> QueryOperation:
        pass

    def delete_rcv(self, kw: Dict) -> QueryOperation:
        pass

    def delete_xpx(self, kw) -> QueryOperation:
        pass

    def update(self, kw: Dict) -> QueryOperation:
        pass

    def quit(self) -> None:
        import sys
        sys.exit(0)

    def clear_console(self) -> None:
        pass

    def __call__(self, *args, **kwargs):
        pass


class Report:
    def __init__(self):
        self._logger = logging.getLogger("pfim.Report")
        self._fmt = None
        self._head = None
        self._line = None

    def create_entry(self, *args, **kw):
        pass

class ReportSummary:
    def __init__(self, data: List[float]):
        self._logger = logging.getLogger("pfim.ReportSummary")
        self._data = data
        self._compute()

    def _compute(self):
        self._count = len(self._data)
        self._min = min(self._data)
        self._max = max(self._data)
        self._median = statistics.median(self._data)
        self._mean = statistics.fmean(self._data)
        self._stdev = statistics.stdev(self._data)

    def __str__(self):
        summary = f"""
        SUMMARY
        -------
            Count: {self._count}
            Minimum: {self._min}
            Maximum: {self._max}
            Average: {self._mean}
            Median: {self._median}
            Stdev: {self._stdev}
        """
        return summary


class PfimCore:
    """PFIM Core class."""
    
    prolog = ""
    epilog = ""

    def __init__(self):
        self._logger = logging.getLogger("pfim.PfimCore")
        self._mode = None
        self._output = None
        self._query_history = Queue(maxsize=128)

    """ def record(self, *args, **kwargs) -> None:
        pass

    def update(self, *args, **kwargs) -> str:
        pass

    def delete(self, *args, **kwargs) -> str:
        pass

    def report(self, *args, **kwargs) -> Report:
        pass """

    def make_output(self) -> Output:
        pass

    def write_output(self, file=sys.stdout):
        pass


    def create_query(self, cmd: PfimQueryCmdEnum, kw: Dict) -> str:
        """Create a new query."""
        query = None
        # addgrp
        # addcmds = (record-rcv|record-xpx)
        # addOpts = [recDate|recTag]
        if cmd == PfimQueryCmdEnum.RECORD_RCV:
            # TODO: make query then return it immediatly
            return query
        if cmd == PfimQueryCmdEnum.RECORD_XPX:
            # TODO: make query then return it immediatly
            return query

        # showcmds=(show|show-rcv|show-spent)
        # showOpts=[sort-(date|tag|amount)]|[after-date|before-date|on-date|
        #   --desc]
        if cmd == PfimQueryCmdEnum.SHOW:
            # TODO: make query then return it immediatly
            return query
        if cmd == PfimQueryCmdEnum.SHOW_RCV:
            # TODO: make query then return it immediatly
            return query
        if cmd == PfimQueryCmdEnum.SHOW_XPX:
            # TODO: make query then return it immediatly
            return query
        
        # upcmds = (update|update-rcv|update-spent)
        # upOpts = [(old-tag, new-tag)|(old-date,new-date)|(old-amount,
        #   new-amount)]
        if cmd == PfimQueryCmdEnum.UPDATE:
            # TODO: make query then return it immediatly
            return query
        if cmd == PfimQueryCmdEnum.UPDATE_RCV:
            # TODO: make query then return it immediatly
            return query
        if cmd == PfimQueryCmdEnum.UPDATE_XPX:
            # TODO: make query then return it immediatly
            return query

        # rmcmds = (delete|delete-rcv|delete-spent)
        # rmOpts = [target-tag|target-date|target-mount]
        if cmd == PfimQueryCmdEnum.DELETE:
            # TODO: make query then return it immediatly
            return query
        if cmd == PfimQueryCmdEnum.DELETE_RCV:
            # TODO: make query then return it immediatly
            return query
        if cmd == PfimQueryCmdEnum.DELETE_XPX:
            # TODO: make query then return it immediatly
            return query


del _filehandler, _consolehandler, _formatter

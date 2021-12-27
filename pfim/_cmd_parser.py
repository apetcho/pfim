from curses.panel import update_panels
from ._version import PFIM_VERSION
from datetime import date


def _cmd_parser():
    import argparse
    DESCRIPTION = """
    pfim is a small command-line tool for tracking personal finance. It track
    your incomes and expenses, and can show a report based a given request
    through its sub-commands and options. pfim can be use as ordinary command
    line tool or can be placed in an interactive mode throught the -i or 
    --interactive option. The --list option list all the sub-commands that come
    with pfim. The --help-cmd option show the help for specific sub-command. 
    """
    parser = argparse.ArgumentParser(
        prog="pfim",
        usage="%(prog)s [OPTIONS]",
        description=DESCRIPTION,
        epilog="",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    #pfim [-v | --version]
    
    parser.add_argument("-v", "--version", action="version",
        version="%(prog)s " + f"{PFIM_VERSION}")
    parser.add_argument("-i", "--interactive", dest="interactive",
        action="store_true", help="Switch to interactive mode")
    parser.add_argument("-l", "--list", action="store_true", dest="lstCmd",
        help="List all pfim sub-commands")
    parser.add_argument("--help-cmd", type=str, dest="helpCmd", metavar="cmd",
        help="Show documentation for a given command")

    # sub-commands parser
    subparsers = parser.add_subparsers(title="pfim sub-commands")

    # -- record subcommand
    recparser = subparsers.add_parser(
        name="record",
        usage="\n\tpfim record [OPTIONS]",
        help="Record an income or expense entry")
    recparser.add_argument("--date", type=str, dest="recdate",
        metavar="YYYY-MM-DD", default=date.today().isoformat(),
        help="Specify the date for this record. Default is current date")
    recparser.add_argument("--tag", type=str, dest="rectag", metavar="TAG",
        help="Tag this record. [default: N/A]", default="N/A")
    recparser.add_argument("--descr", type=str, dest="descr",
        metavar="TEXT", default="N/A",
        help="Add short the description for this record. [default: N/A]")
    recpex = recparser.add_mutually_exclusive_group()
    recpex.add_argument("--exp", type=float, dest="expense",
        metavar="VALUE",
        help="This record is an expense of this VALUE")
    recpex.add_argument("--inc", type=float, dest="income",
        metavar="VALUE",
        help="This record is an income of this VALUE")
    
    # -- report subcommand
    repparser = subparsers.add_parser(
        name="report",
        usage="\n\tpfim report [OPTIONS]",
        help="Show report for a given query")
    repparser.add_argument("--sort-date", action="store_true",
        dest="sortDate",
        help="Sort the query result by date")
    repparser.add_argument("--sort-tag", action="store_true", dest="sortTag",
        help="Sort the query result by tag")
    repparser.add_argument("--sort-amount", action="store_true",
        dest="sortAmount",
        help="Sort the query result by amount, i.e expense or income value")
    repparser.add_argument("--before", type=str, dest="beforeQuery",
        metavar="YYYY-MM-DD",
        help="Show report for records whose date pre-date YYYY-MM-DD")
    repparser.add_argument("--after", type=str, dest="afterQuery",
        metavar="YYYY-MM-DD",
        help="Show report for records whose date post-date YYYY-MM-DD")
    repparser.add_argument("--on", type=str, dest="onQuery",
        metavar="YYYY-MM-DD",
        help="Show report for records for the given date YYYY-MM-DD")
    repparser.add_argument("--for-tag", type=str, dest="tagQuery",
        metavar="TAG",
        help="Show report for records for the given TAG")
    repparser.add_argument("--for-exp", action="store_true", dest="expQuery",
        help="Show report only for records for expenses")
    repparser.add_argument("--for-inc", action="store_true", dest="incQuery",
        help="Show report only for records for incomes")
    repparser.add_argument("--all", action="store_true", dest="allQuery",
        help="Show report for all records")
    
    # -- update subcommand parser
    # upcmds = (update|update-rcv|update-spent)
    # upOpts = [(old-tag, new-tag)|(old-date,new-date)|(old-amount,
    #   new-amount)]
    updparser = subparsers.add_parser(
        name="update",
        formatter_class=argparse.RawTextHelpFormatter,
        usage="\n\tpfim update [OPTIONS]",
        help="Update record(s) for given query")
    updparser.add_argument("--expense", nargs=3, dest="upExpense",
        metavar="",
        help=("Update the income for a given date. \nThe format is: "
            "--expense YYYY-DD-MM OLD_VALUE NEW_VALUE"
            "\n\tExample: pfim update --expense 2021-12-19 230.15 320.10"))
    updparser.add_argument("--income", nargs=3, dest="upIncome",
        metavar="",
        help=("Update the income for a given date. \nThe format is: "
            "--expense YYYY-DD-MM OLD_VALUE NEW_VALUE"
            "\n\tExample: pfim update --income 2021-03-23 780.25 1125.10"))
    updparser.add_argument("--tag", nargs=3, dest="upTag",
        metavar="",
        help=("Update the tag for a given date. \nThe format is: "
            "--tag YYYY-DD-MM OLD_TAG NEW_TAG"
            "\n\tExample: pfim update --tag 2021-05-13 freeL work"))
    updparser.add_argument("--descr", nargs=4, dest="upDescr",
        metavar="",
        help=(  """Update a record description for given date.
The format is: --desc YYYY-MM-DD OLD_DESCR NEW_DESCR
\tExample:  2022-02-17 'Concert reservation' 'Hotel booking for PyCon'"""))

    # -- delete subcommand parser
    # # delcmds = (delete|delete-rcv|delete-spent)
    # # delOpts = [target-tag|target-date|target-mount]
    rmparser = subparsers.add_parser(
        name="delete",
        usage="\n\tpfim delete [OPTIONS]",
        help="Delete record(s) for given query")
    rmparser.add_argument("--exp", type=float, dest="rmExpense",
        metavar="VALUE",
        help="Delete record(s) where expense is VALUE")
    rmparser.add_argument("--inc", type=float, dest="rmIncome",
        metavar="VALUE",
        help="Delete record(s) where income is VALUE")
    rmparser.add_argument("--tag", type=str, dest="rmTag",
        metavar="TAG",
        help="Delete record where tag is TAG")
    rmparser.add_argument("--on", type=str, dest="rmDate",
        metavar="YYYY-MM-DD",
        help="Delete record where date is the date provided in YYYY-MM-DD format")
    rmparser.add_argument("--before", type=str, dest="rmBDate",
        metavar="YYYY-MM-DD",
        help="Delete all record(s) before a given date in YYYY-MM-DD format")
    rmparser.add_argument("--after", type=str, dest="rmADate",
        metavar="YYYY-MM-DD",
        help="Delete all records(s) after a given date in YYYY-MM-DD format")
    rmparser.add_argument("--all", action="store_true", dest="rmAll",
        help="Delete all records")
    
    return parser

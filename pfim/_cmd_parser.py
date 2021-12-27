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
        help="Record an income or expense entry",
        usage=(
            "pfim record [--date=YYYY-MM-DD][--tag=TAG][--descr=TEX] "
            "(--exp=VALUE | --inc=VALUE)"))
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
    delparser = subparsers.add_parser(
        name="delete",
        help="Delete record(s) for given query")

    # recparser.add_argument("--tag", type=str, dest="extag", metavar="TAG",
    #     help="Tag a record")
    # recparser.add_argument("-descr", "--description", type=str)
    # recex = recparser.add_mutually_exclusive_group()
    # recex.add_argument("--expense", type=float, dest="expense", metavar="VALUE", help="Record the expense of thie VALUE")

    #parser.add_argument("--fancy-output", action="store_true",
    #    dest="fancy", help="Toggle PFIM into fancy output mode")

    # addgrp
    # addcmds = (rec-rcv|rec-xpx)
    # addOpts = [date|tag]
    # addgrp = parser.add_argument_group(
    #     "Record income/expense commands and options")
    # addgrp.add_argument("--tag", nargs="?", type=str, dest="recTag",
    #     help=("Attach a tag to this received. Possible value are RCV and "  
    #         "XPX. [default: RCV]"), default="RCV", metavar="TAG",
    #         choices=["RCV", "XPX"])
    # addgrp.add_argument("--date", nargs="?", type=str, dest="recDate",
    #     help="Add the specific date for the received amount",
    #     default="current date", metavar="YYYY-MM-DD")
    # addgrp.add_argument("--description", type=str, dest="Description",
    #     help='Short description for a new record. [default: "N/A"]',
    #     default="N/A", metavar="TEXT")
    # addex = addgrp.add_mutually_exclusive_group()
    # addex.add_argument("-record-rcv", type=float, dest="rcv",
    #     help="The actual amount you received", metavar="VALUE")
    # addex.add_argument("-record-xpx", type=float, dest="xpx",
    #     help="The actual amount you spent", metavar="VALUE")

    # # showcmds=(show|show-rcv|show-spent)
    # # showopts=[sort-(date|tag|amount)]|[after-date|before-date|on-date|--desc]
    # showgrp = parser.add_argument_group("Report showing commands and options")
    # showgrp.add_argument("--sort-date", action="store_true", dest="sortDate",
    #     help="Show output ordered by date")
    # showgrp.add_argument("--sort-tag", action="store_true", dest="sortTag",
    #     help="Show output ordered by tag")
    # showgrp.add_argument("--sort-val", action="store_true", dest="sortVal",
    #     help="Show output ordered by income/expense value")
    # showgrp.add_argument("--desc", action="store_true", dest="sortDesc",
    #     help="Sort in descending order. The default sorting order is ascending")
    # showgrp.add_argument("--before-date", type=str, dest="beforeDate",
    #     help="Show records before a specific date",
    #     metavar="YYYY-MM-DD")
    # showgrp.add_argument("--after-date", type=str, dest="afterDate",
    #     help="Show records after a specific date",
    #     metavar="YYYY-MM-DD")
    # showgrp.add_argument("--on-date", type=str, dest="onDate",
    #     help="Show record on a specific date",
    #     metavar="YYYY-MM-DD")
    # showex = showgrp.add_mutually_exclusive_group()
    # showex.add_argument("-show", action="store_true", dest="show",
    #     help="Show all records in the database")
    # showex.add_argument("-show-recv", action="store_true", dest="showRCV",
    #     help="Show all records in the database corresponding to incomes")
    # showex.add_argument("-show-xpx", action="store_true", dest="showXPX",
    #     help="Show all records in the database corresponting to expenses")
    
    # updategrp = parser.add_argument_group("Update record commands and options")
    # # upcmds = (update|update-rcv|update-spent)
    # # upOpts = [(old-tag, new-tag)|(old-date,new-date)|(old-amount,new-amount)]
    # updategrp.add_argument("--old-tag", type=str, dest="oldTag", metavar="TAG1",
    #     help="Previous tag to be updated")
    # updategrp.add_argument("--new-tag", type=str, dest="newTag", metavar="TAG2",
    #     help="New tag to update the old one")
    # updategrp.add_argument("--old-date", type=str, dest="oldDate", 
    #     metavar="YYYY-MM-DD", help="Previous date to be updated")
    # updategrp.add_argument("--new-date", type=str, dest="newDate", 
    #     metavar="YYYY-MM-DD", help="New date to update the old one")
    # updategrp.add_argument("--old-val", type=float, dest="oldVal", 
    #     metavar="VALUE1",
    #     help="Previous amount value to be updated")
    # updategrp.add_argument("--new-val", type=float, dest="newVal", 
    #     metavar="VALUE2", help="New amount value to update the old one")
    # updatex = updategrp.add_mutually_exclusive_group()
    # updatex.add_argument("-update", action="store_true", default="update",
    #     help="Update record(s)")
    # updatex.add_argument("-update-rcv", action="store_true", dest="updateRCV",
    #     help="Update record(s) corresponding to income")
    # updatex.add_argument("-update-xpx", action="store_true", 
    #     dest="updateXPX", help="Update record(s) corresponding to expense")
    
    # # delcmds = (delete|delete-rcv|delete-spent)
    # # delOpts = [target-tag|target-date|target-mount]
    # rmgrp = parser.add_argument_group("Delete commands and options")
    # rmgrp.add_argument("--target-tag", type=str, dest="targetTag",
    #     metavar="TAG", help="Delete record(s) for a specific tag")
    # rmgrp.add_argument("--target-date", type=str, dest="targetDate",
    #     metavar="YYYY-MM-DD", help="Delete record(s) for a specific date")
    # rmgrp.add_argument("--target-val", type=float, dest="targetVal",
    #     metavar="VALUE",
    #     help="Delete record(s) for a specific income/expense value")
    # rmex = rmgrp.add_mutually_exclusive_group()
    # rmex.add_argument("-delete", action="store_true", dest="delete",
    #     help="Delete record(s)")
    # rmex.add_argument("-delete-rcv", action="store_true", dest="deleteRCV",
    #     help="Delete record(s) corresponding to incomes")
    # rmex.add_argument("-delete-xpx", action="store_true", 
    #     dest="deleteXPX", help="Delete record(s) corresponding to expenses")

    return parser

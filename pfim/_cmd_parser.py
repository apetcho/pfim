from ._version import PFIM_VERSION

def _cmd_parser():
    import argparse
    USAGE = """
    pfim [-h | --help] [-v | --version] [--interactive]
    pfim sub-command [opt1, ...]
        
The available sub-commands are:
    -rcv, -spent, -show, -show-rcv, -show-spent, -update, -update-rcv,
    -update-spent, -delete, -delete-rcv, -delete-spent

The sub-commands options are describe below.
    """
    parser = argparse.ArgumentParser(
        prog="pfim",
        usage=USAGE,
        description="PFIM: Personal Finance Manager",
        epilog=""
    )
    # group0
    #pfim [-v | --version]
    parser.add_argument("-v", "--version", action="version",
        version="%(prog)s " + f"{PFIM_VERSION}")
    parser.add_argument("-i", "--interactive", dest="imode",
        action="store_true", help="Switch to interactive mode")
    parser.add_argument("--fancy-output", action="store_true",
        dest="fancy", help="Toggle into fancy output mode")

    # group1
    addgrp = parser.add_argument_group(
        "Record adding commands and options")
    addgrp.add_argument("--tag", nargs="?", type=str, dest="atag",
        help=("Attach a tag to this received. Default is RCV if money "  
            "received"), default="RCV", metavar="TAG")
    addgrp.add_argument("--date", nargs="?", type=str, dest="aedate",
        help="Add the specific date for the received amount",
        default="current date", metavar="YYYY-MM-DD")
    addex = addgrp.add_mutually_exclusive_group()
    addex.add_argument("-rcv", type=float, dest="rcv",
        help="The actual amount you received", metavar="AMOUNT")
    addex.add_argument("-spent", type=float, dest="aspent",
        help="The actual amount you spent", metavar="AMOUNT")

    # showcmds=(show|show-rcv|show-spent)
    # showopts=[sort-(date|tag|amount)]|[after-date|before-date|on-date|--desc]
    showgrp = parser.add_argument_group("Report showing commands and options")
    showgrp.add_argument("--sort-date", action="store_true", dest="sortDate",
        help="Show output ordered by date")
    showgrp.add_argument("--sort-tag", action="store_true", dest="sortTag",
        help="Show output ordered by tag")
    showgrp.add_argument("--sort-amount", action="store_true", dest="sortAmount",
        help="Show output ordered by amount value")
    showgrp.add_argument("--desc", action="store_true", dest="sortDesc",
        help="Sort in descending order. The default sorting order is ascending")
    showgrp.add_argument("--before-date", type=str, dest="beforeDate",
        help="Show records before a specific date",
        metavar="YYYY-MM-DD")
    showgrp.add_argument("--after-date", type=str, dest="afterDate",
        help="Show records after a specific date",
        metavar="YYYY-MM-DD")
    showgrp.add_argument("--on-date", type=str, dest="onDate",
        help="Show record on a specific date",
        metavar="YYYY-MM-DD")
    showex = showgrp.add_mutually_exclusive_group()
    showex.add_argument("-show", action="store_true", dest="show",
        help="Show all records in the database")
    showex.add_argument("-show-recv", action="store_true", dest="showRcv",
        help="Show all records in the database corresponding to incomes")
    showex.add_argument("-show-spent", action="store_true", dest="showSpent",
        help="Show all records in the database corresponting to expenses")
    
    # group4
    # group5
    # group6
    updategrp = parser.add_argument_group("Update record commands and options")
    # upcmds = (update|update-rcv|update-spent)
    # upOpts = [(old-tag, new-tag)|(old-date,new-date)|(old-amount,new-amount)]
    updategrp.add_argument("--old-tag", type=str, dest="oldTag", metavar="TAG1",
        help="Previous tag to be updated")
    updategrp.add_argument("--new-tag", type=str, dest="newTag", metavar="TAG2",
        help="New tag to update the old one")
    updategrp.add_argument("--old-date", type=str, dest="oldDate", 
        metavar="YYYY-MM-DD", help="Previous date to be updated")
    updategrp.add_argument("--new-date", type=str, dest="newDate", 
        metavar="YYYY-MM-DD", help="New date to update the old one")
    updategrp.add_argument("--old-amount", type=float, dest="oldAmount", 
        metavar="VALUE1",
        help="Previous amount value to be updated")
    updategrp.add_argument("--new-amount", type=float, dest="newAmount", 
        metavar="VALUE2", help="New amount value to update the old one")
    updatex = updategrp.add_mutually_exclusive_group()
    updatex.add_argument("-update", action="store_true", default="update",
        help="Update record(s)")
    updatex.add_argument("-update-rcv", action="store_true", dest="updateRcv",
        help="Update record(s) corresponding to income")
    updatex.add_argument("-update-spent", action="store_true", 
        dest="updateSpent", help="Update record(s) corresponding to expense")
    
    # group7
    # 30. pfim -delete-all
    # 31. pfim -delete --target-tag=TAG1
    # 32. pfim -delete --target-date=YYYY-MM-DD
    # 33. pfim -delete-rcv --target-amount=VALUE
    # 34. pfim -deltte-spent --target-amount=VALUE


    return parser

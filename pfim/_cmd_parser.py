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
    group1 = parser.add_argument_group(
        "Add a new amount received or spent to the database")
    group1.add_argument("--tag", nargs="?", type=str, dest="atag",
        help=("Attach a tag to this received. Default is RCV if money "  
            "received"), default="RCV", metavar="TAG")
    group1.add_argument("--date", nargs="?", type=str, dest="aedate",
        help="Add the specific date for the received amount",
        default="current date", metavar="YYYY-MM-DD")
    addex = group1.add_mutually_exclusive_group()
    addex.add_argument("-rcv", type=float, dest="rcv",
        help="The actual amount you received", metavar="AMOUNT")
    addex.add_argument("-spent", type=float, dest="aspent",
        help="The actual amount you spent", metavar="AMOUNT")

    # group2
    # group3
    group2 = parser.add_argument_group("Show report")
    group2.add_argument("--sort-date", action="store_true", dest="sortDate",
        help="Show output ordered by date")
    group2.add_argument("--sort-tag", action="store_true", dest="sortTag",
        help="Show output ordered by tag")
    group2.add_argument("--sort-amount", action="store_true", dest="sortAmount",
        help="Show output ordered by amount value")
    group2.add_argument("--desc", action="store_true", dest="sortDesc",
        help="Sort in descending order. The default sorting order is ascending")
    group2.add_argument("--before-date", type=str, dest="beforeDate",
        help="Show records before a specific date",
        metavar="YYYY-MM-DD")
    group2.add_argument("--after-date", type=str, dest="afterDate",
        help="Show records after a specific date",
        metavar="YYYY-MM-DD")
    group2.add_argument("--on-date", type=str, dest="onDate",
        help="Show record on a specific date",
        metavar="YYYY-MM-DD")
    showex = group2.add_mutually_exclusive_group()
    showex.add_argument("-show", action="store_true", dest="show",
        help="Show all records in the database")
    showex.add_argument("-show-recv", action="store_true", dest="showRcv",
        help="Show all records in the database corresponding to incomes")
    showex.add_argument("-show-spent", action="store_true", dest="showSpent",
        help="Show all records in the database corresponting to expenses")
    # cmds = (show|show-rcv|show-spent)
    # opts = [sort-(date|tag|amount)]|[after-date|before-date|on-date|--desc]
    # group4
    # 15. pfim --show-earned
    # 16. pfim --show-earned --sort-date
    # 17. pfim --show-earned --sort-tag
    # 18. pfim --show-earned --sort-amount
    # 19. pfim --show-earned --before-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
    # 20. pfim --show-earned --after-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
    # group5
    # 21. pfim --show-spent
    # 22. pfim --show-spent --sort-date
    # 23. pfim --show-spent --sort-tag
    # 24. pfim --show-spent --sort-amount
    # 24. pfim --show-spent --before-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
    # 25. pfim --show-spent --after-date=YYYY-MM-DD [--sort-date|--sort-date|--sort-amount]
    # group6
    # 26. pfim --update --tag=TAG1 --new-tag=TAG2
    # 27. pfim --update --date=YYYY-MM-DD
    # 28. pfim --update --earned --amount=VALUE1 --new-amount=VALUE2
    # 29. pfim --update --spent --amount=VALUE2 --new-amount=VALUE2
    # group7
    # 30. pfim --delete-all
    # 31. pfim --delete --tag=TAG1
    # 32. pfim --delete --date=YYYY-MM-DD
    # 33. pfim --delete --earned --amount=VALUE
    # 34. pfim --deltte --spent --amount=VALUE


    return parser

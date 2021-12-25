from ._version import PFIM_VERSION

def _cmd_parser():
    import argparse
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
    pfim --show-spent --before-date=YYYY-MM-DD [--sort-date|--sort-date
        --sort-amount]
    pfim --show-spent --after-date=YYYY-MM-DD [--sort-date|--sort-date|
        --sort-amount]

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
    # group0
    #pfim [-v | --version]
    parser.add_argument("-v", "--version", action="version",
        version="%(prog)s " + f"{PFIM_VERSION}")
    parser.add_argument("-i", "--interactive", dest="imode",
        action="store_true", help="Switch to interactive mode")
    parser.add_argument("--fancy-output", action="store_true",
        dest="cfg", help="Toggle into fancy output mode")

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
    addex.add_argument("--rcv", type=float, dest="arcv",
        help="The actual amount you received", metavar="AMOUNT")
    addex.add_argument("--spent", type=float, dest="aspent",
        help="The actual amount you spent", metavar="AMOUNT")

    # group2
    # group3
    # group4
    # group5
    # group6
    # group7

    return parser

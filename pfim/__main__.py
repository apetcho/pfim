from ._cmd_parser import _cmd_parser
from .pfim import PfimCore
from .pfim import PfimEntry
from .pfim import PfimData
from .pfim import InteractivePfim
from .pfim import Output, OutputBeautify
from .pfim import Report, ReportSummary

# import _version
from ._version import PFIM_VERSION

ipfim = InteractivePfim()
__all__ = ["get_version", "cpfim", "ipfim"]


def _cpfim():
    pass

def _ipfim():
    pass


def main():
    import sys 
    parser = _cmd_parser()
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()

    # request for the list of pfim sub-commands
    if args.lstCmd:
        pass

    # request for documentation of a given command
    # The available sub-commands are:
    # -record-rcv, -record-xpx, -show, -show-rcv, -show-xpx, -update,
    # -update-rcv, -update-xpx, -delete, -delete-rcv, -delete-xpx
    if args.helpCmd:
        cmdlist = ["record", "show", "update", "delete"]
        if args.helpCmd not in cmdlist:
            print("Unknown command", file=sys.stderr)   # XXX

        # show documentation of record command
        if args.record:
            pass
        # show documentation of show command
        if args.show:
            pass
        if args.update:
            pass
        if args.delete:
            pass
        
    # We are not in interactive mode
    if not args.interactive:
        pass

    # We are in interactive mode
    if args.interactive:
        pass

main()

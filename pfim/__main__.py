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
        
    if args.fancy:
        _ipfim()
        print("Fancy output turned ON")
    else:
        _cpfim()
        print("Fancy output turned OFF")  

main()

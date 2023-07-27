from .Lakeshore335 import Lakeshore335


def main():
    import sys
    import tango.server

    args = ["Lakeshore335"] + sys.argv[1:]
    tango.server.run((Lakeshore335,), args=args)

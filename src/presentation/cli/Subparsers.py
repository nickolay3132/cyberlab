from argparse import _SubParsersAction


class Subparsers:
    def __init__(self, subparsers: _SubParsersAction):
        self.subparsers = subparsers

    def init(self):
        for method_name in dir(self):
            if method_name.startswith("add_") and method_name.endswith("_subparser"):
                method = getattr(self, method_name)
                if callable(method):
                    method()
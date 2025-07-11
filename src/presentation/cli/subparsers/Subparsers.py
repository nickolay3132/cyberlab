class Subparsers:
   def init(self):
        for method_name in dir(self):
            if method_name.startswith("add_") and method_name.endswith("_subparser"):
                method = getattr(self, method_name)
                if callable(method):
                    method()
"""
Program that only prevents an argument thrown by topdown.py from being repeated.

@date:      Jan-2021
@version:   1.0
"""
import argparse

class DontRepeat(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if getattr(namespace, self.dest, self.default) is not self.default:
            # show error
            parser.error(option_string + " appears several times. Only one time is allowed.")
        setattr(namespace, self.dest, values)
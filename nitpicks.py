"""
Checks for bare excepts, including the cases:
except Exception:
except BaseException:
except Exception as myname:
etc.
"""

import re

CHECKER_NAME = 'bare_except_check'
CHECKER_VERSION = '1.0.0'


def add_checker_metadata(check):
    "Flake8 expects checkers to have `name` and `version` attrs"
    check.name = CHECKER_NAME
    check.version = CHECKER_VERSION
    return check


@add_checker_metadata
def generic_exception_check(logical_line):
    regex = re.compile(r'except\s+(Base)?Exception(\s+as\s+\w+)?\s*:')
    match = regex.match(logical_line)
    if match:
        # flake8 expects (column_number, error_string)
        # column is always 0 b/c leading space is stripped from the logical line
        yield (0, 'B1 Over-generic exception used')

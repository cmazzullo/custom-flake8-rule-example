from unittest import TestCase

from nitpicks import (
    CHECKER_NAME,
    CHECKER_VERSION,
    generic_exception_check,
)


class TestBareExceptCheck(TestCase):
    def test_line_without_error(self):
        line = 'print("hi")'
        errors = list(generic_exception_check(line))
        self.assertEqual(len(errors), 0)

    def test_generic_exception_is_not_detected(self):
        "This is already covered by E722"
        line = 'except:'
        errors = list(generic_exception_check(line))
        self.assertEqual(len(errors), 0)

    def test_except_Exception_is_detected(self):
        line = 'except Exception:'
        errors = list(generic_exception_check(line))
        self.assertEqual(len(errors), 1)

    def test_check_function_has_metadata_attributes(self):
        "Flake8 needs check funcs to have the `name` and `version` attributes"
        self.assertEqual(generic_exception_check.name, CHECKER_NAME)
        self.assertEqual(generic_exception_check.version, CHECKER_VERSION)

    def test_checker_reports_column_number(self):
        """Column number should be 0 because `except` must be on a line alone.

        Indentation won't change this b/c it's stripped from the logical_line.
        """
        line = 'except Exception:'
        errors = list(generic_exception_check(line))
        self.assertEqual(len(errors), 1)
        self.assertEqual(len(errors[0]), 2)  # tuple of column and err_msg
        column = errors[0][0]
        self.assertEqual(column, 0)

    def test_regex_edge_cases(self):
        error_cases = [
            'except BaseException:',
            'except BaseException as bex:',
            'except  \tBaseException   as     bex\t :',
            'except Exception:',
            'except Exception : ',
        ]
        for case in error_cases:
            errors = list(generic_exception_check(case))
            self.assertEqual(len(errors), 1)

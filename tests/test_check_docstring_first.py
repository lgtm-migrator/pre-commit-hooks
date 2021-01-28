# 3rd party
import pytest
from consolekit.testing import CliRunner, Result
from domdf_python_tools.paths import PathPlus

# this package
from pre_commit_hooks.check_docstring_first import check_docstring_first, main

# Contents, expected, expected_output
TESTS = (
		# trivial
		(b'', 0, ''),
		# Acceptable
		(b'"foo"', 0, ''),
		# Docstring after code
		(
				b'from __future__ import unicode_literals\n'
				b'"foo"\n',
				1,
				'{filename}:2 Module docstring appears after code '
				'(code seen on line 1).\n',
				),
		# Test double docstring
		(
				# This one should be valid now
				b'"The real docstring"\n'
				b'from __future__ import absolute_import\n'
				b'"fake docstring"\n',
				0,
				'',
				),
		# Test multiple lines of code above
		(
				b'import os\n'
				b'import sys\n'
				b'"docstring"\n',
				1,
				'{filename}:3 Module docstring appears after code '
				'(code seen on line 1).\n',
				),
		# String literals in expressions are ok.
		(b'x = "foo"\n', 0, ''),
		)

all_tests = pytest.mark.parametrize("contents, expected, expected_out", TESTS)


@all_tests
def test_unit(capsys, contents, expected, expected_out):
	assert check_docstring_first(contents) == expected
	assert capsys.readouterr()[0] == expected_out.format(filename="<unknown>")


@all_tests
def test_integration(tmp_pathplus: PathPlus, contents, expected, expected_out):
	path = tmp_pathplus / "test.py"
	path.write_bytes(contents)

	runner = CliRunner()
	result: Result = runner.invoke(main, args=[str(path)])
	assert result.exit_code == expected
	assert result.stdout == expected_out.format(filename=str(path))


def test_arbitrary_encoding(tmp_pathplus: PathPlus):
	path = tmp_pathplus / "f.py"
	contents = '# -*- coding: cp1252\nx = "£"'.encode("cp1252")
	path.write_bytes(contents)

	runner = CliRunner()
	result: Result = runner.invoke(main, args=[str(path)])
	assert result.exit_code == 0

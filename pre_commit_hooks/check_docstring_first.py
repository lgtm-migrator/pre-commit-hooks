"""
Based on https://github.com/pre-commit/pre-commit-hooks/blob/master/pre_commit_hooks/check_docstring_first.py

Modified to permit multiple "docstring" like objects
as long as the first one is at the top of the file.
This is useful when writing Sphinx docstrings for attributes, variables etc.
"""

# stdlib
import argparse
import io
import tokenize
from tokenize import tokenize as tokenize_tokenize
from typing import Optional, Sequence

# this package
from pre_commit_hooks.util import FAIL, PASS

__all__ = ["check_docstring_first", "main"]

NON_CODE_TOKENS = frozenset((
		tokenize.COMMENT,
		tokenize.ENDMARKER,
		tokenize.NEWLINE,
		tokenize.NL,
		tokenize.ENCODING,
		))


def check_docstring_first(src: bytes, filename: str = "<unknown>") -> int:
	"""
	Returns nonzero if the source has what looks like a docstring that is
	not at the beginning of the source.

	A string will be considered a docstring if it is a STRING token with a
	col offset of 0.
	"""

	found_docstring_line = None
	found_code_line = None

	tok_gen = tokenize_tokenize(io.BytesIO(src).readline)

	for tok_type, _, (sline, scol), _, _ in tok_gen:
		# Looks like a docstring!
		if tok_type == tokenize.STRING and scol == 0:
			if found_docstring_line is not None:
				pass
			elif found_code_line is not None:
				print(
						f'{filename}:{sline} Module docstring appears after code '
						f'(code seen on line {found_code_line}).',
						)
				return FAIL
			else:
				found_docstring_line = sline
		elif tok_type not in NON_CODE_TOKENS and found_code_line is None:
			found_code_line = sline

	return PASS


def main(argv: Optional[Sequence[str]] = None) -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("filenames", nargs='*')
	args = parser.parse_args(argv)

	retv = PASS

	for filename in args.filenames:
		with open(filename, "rb") as f:
			contents = f.read()
		retv |= check_docstring_first(contents, filename=filename)

	return retv

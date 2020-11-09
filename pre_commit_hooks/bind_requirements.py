# stdlib
import argparse
import sys
from typing import Optional, Sequence

# 3rd party
from shippinglabel.pypi import bind_requirements

# this package
from pre_commit_hooks.util import PASS

__all__ = ["main"]


def main(argv: Optional[Sequence[str]] = None) -> int:
	parser = argparse.ArgumentParser(
			description="Bind unbound requirements to the latest version on PyPI, and any later versions.",
			)
	parser.add_argument("filenames", nargs='*', help="Filenames to bind requirements for.")
	parser.add_argument(
			"--specifier",
			type=str,
			default=">=",
			help="The version specifier symbol to use. (default: %(default)s)",
			)

	args = parser.parse_args(argv)
	retv = PASS

	for filename in args.filenames:
		ret_for_file = bind_requirements(filename, args.specifier)

		if ret_for_file:
			print(f"Binding requirements for {filename}")

		retv |= ret_for_file

	if not retv:
		print("Up to date.")

	return retv


if __name__ == "__main__":
	sys.exit(main())

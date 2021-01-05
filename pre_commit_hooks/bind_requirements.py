# stdlib
import argparse
import sys
from typing import Optional, Sequence

# 3rd party
import requests
from shippinglabel.pypi import bind_requirements
from urllib3.exceptions import MaxRetryError, NewConnectionError  # type: ignore

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
		try:
			ret_for_file = bind_requirements(filename, args.specifier)

			if ret_for_file:
				print(f"Binding requirements for {filename}")

		except (NewConnectionError, MaxRetryError, requests.exceptions.ConnectionError) as e:
			print(f"Error binding requirements for {filename}: {str(e)}")
			ret_for_file = 1

		retv |= ret_for_file

	if not retv:
		print("Up to date.")

	return retv


if __name__ == "__main__":
	sys.exit(main())

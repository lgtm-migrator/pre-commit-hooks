# stdlib
import argparse
import sys
from typing import List, Optional, Sequence, Set

# 3rd party
from apeye.url import SlumberURL
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

# this package
from pre_commit_hooks.util import FAIL, PASS, read_requirements

__all__ = ["get_latest", "bind_requirements", "main", "PYPI_API"]

PYPI_API = SlumberURL("https://pypi.org/pypi/")


def get_latest(pypi_name: str) -> str:
	"""
	Returns the version number of the latest release on PyPI for the given project.

	:param pypi_name:
	"""

	query_url = PYPI_API / pypi_name / "json"
	return str(query_url.get()['info']['version'])


def bind_requirements(filename: PathLike, specifier: str = ">=") -> int:
	"""
	Bind unbound requirements in the given file to the latest version on PyPI, and any later versions.

	:param filename: The requirements.txt file to bind requirements in.
	:param specifier: The requirements specifier symbol to use.

	:return: ``1`` if the file was changed; ``0`` otherwise.
	"""

	ret = PASS
	filename = PathPlus(filename)
	req_list, invalid_lines, comments = read_requirements(filename)
	requirements: Set[Requirement] = set(req_list)

	for req in requirements:
		if not req.specifier:
			ret |= FAIL
			latest_version = get_latest(req.name)
			req.specifier = SpecifierSet(f"{specifier}{latest_version}")

	sorted_requirements = sorted(requirements, key=lambda r: r.name.casefold())
	buf: List[str] = [*comments, *invalid_lines]

	for req in sorted_requirements:
		buf.append(str(req))

	if buf != list(filter(lambda x: x != '', filename.read_text().splitlines())):
		# print('\n'.join(buf))
		ret |= FAIL
		filename.write_clean('\n'.join(buf))

	return ret


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

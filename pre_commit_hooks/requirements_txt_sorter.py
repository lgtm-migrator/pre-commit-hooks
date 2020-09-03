# stdlib
import argparse
import sys
from typing import List, Optional, Sequence

# 3rd party
from domdf_python_tools.paths import PathLike, PathPlus

# this package
from pre_commit_hooks.util import FAIL, PASS, Requirement, read_requirements

__all__ = ["sort_requirements", "main"]


def sort_requirements(filename: PathLike, allow_git: bool = False) -> int:
	"""
	Sort the requirements in the given file alphabetically.

	:param filename: The file to sort the requirements in.
	:param allow_git: Whether to allow lines that start with ``git+``, which are allowed by pip but not :pep:`508`.
	"""

	ret = PASS
	filename = PathPlus(filename)
	comments: List[str]
	requirements: List[Requirement]
	git_lines: List[str] = []

	requirements, invalid_lines, comments = read_requirements(req_file=filename)

	for line in invalid_lines:
		if line.startswith("git+") and allow_git:
			git_lines.append(line)
		else:
			ret |= FAIL

	if not requirements and not invalid_lines:
		# If the file is only whitespace/newlines/comments exit early
		return PASS

	sorted_requirements = sorted(requirements, key=lambda r: r.name.casefold())

	# find and remove pkg-resources==0.0.0
	# which is automatically added by broken pip package under Debian
	if Requirement("pkg-resources==0.0.0") in sorted_requirements:
		sorted_requirements.remove(Requirement("pkg-resources==0.0.0"))
		ret |= FAIL

	buf: List[str] = [*comments, *git_lines]

	for req in sorted_requirements:
		buf.append(str(req))

	if (requirements != sorted_requirements and buf != filename.read_text().splitlines()) or ret:
		print('\n'.join(buf))
		ret |= FAIL
		filename.write_clean('\n'.join(buf))

	return ret


def main(argv: Optional[Sequence[str]] = None) -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("filenames", nargs='*', help="Filenames to sort.")
	parser.add_argument(
			"--allow-git",
			action="store_true",
			default=False,
			help="allow 'git+' options, which are allowed by pip but not PEP 508.",
			)

	args = parser.parse_args(argv)
	retv = PASS

	for arg in args.filenames:
		ret_for_file = sort_requirements(arg, allow_git=args.allow_git)

		if ret_for_file:
			print(f"Sorting {arg}")

		retv |= ret_for_file

	return retv


if __name__ == "__main__":
	sys.exit(main())

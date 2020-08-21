# stdlib
import argparse
import sys
from typing import List, Optional, Sequence

# 3rd party
from domdf_python_tools.paths import PathLike, PathPlus
from packaging.requirements import InvalidRequirement
from packaging.requirements import Requirement as _Requirement

PASS = 0
FAIL = 1


class Requirement(_Requirement):

	def __eq__(self, other):
		if isinstance(other, _Requirement):
			return (
					self.name == other.name and self.url == other.url and self.extras == other.extras
					and self.specifier == other.specifier and self.marker == other.marker
					)
		else:  # pragma: no cover
			return NotImplemented


def sort_requirements(filename: PathLike, allow_git: bool = False) -> int:

	ret = PASS
	ends_with_newline = False

	filename = PathPlus(filename)

	comments: List[str] = []
	git_lines: List[str] = []
	requirements: List[Requirement] = []
	lines = filename.read_text().split("\n")

	for line in lines:
		if line.startswith("#"):
			comments.append(line)
		elif line.startswith("git+") and allow_git:
			git_lines.append(line)
		elif line:
			try:
				req = Requirement(line)
				if req.name.casefold() not in {r.name.casefold() for r in requirements}:
					requirements.append(req)
			except InvalidRequirement:
				# TODO: Show warning to user
				ret = FAIL
				pass

	if not requirements:
		# If the file is only whitespace/newlines/comments exit early
		return PASS

	if not lines[-1]:
		ends_with_newline = True

	sorted_requirements = sorted(requirements, key=lambda r: r.name.casefold())

	# find and remove pkg-resources==0.0.0
	# which is automatically added by broken pip package under Debian
	if Requirement("pkg-resources==0.0.0") in sorted_requirements:
		sorted_requirements.remove(Requirement("pkg-resources==0.0.0"))

	if sorted_requirements != requirements or not ends_with_newline or ret == FAIL:
		buf: List[str] = [*comments, *git_lines]

		for req in sorted_requirements:
			buf.append(str(req))

		filename.write_clean('\n'.join(buf))
		ret = FAIL

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

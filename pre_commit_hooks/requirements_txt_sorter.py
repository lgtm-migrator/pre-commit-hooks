# stdlib
import argparse
from typing import List, Optional, Sequence

# 3rd party
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
		else:
			return NotImplemented


def fix_requirements(filename: str) -> int:

	ret = PASS
	ends_with_newline = False

	with open(filename, "r", encoding="UTF-8") as fp:

		comments: List[str] = []
		requirements: List[Requirement] = []
		lines = list(fp.read().split("\n"))

		for line in lines:
			if line.startswith("#"):
				comments.append(line)
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
		buf: List[str] = []

		for comment in comments:
			buf.append(comment)

		for req in sorted_requirements:
			buf.append(str(req))

		# buf.append('')

		with open(filename, 'w', encoding="UTF-8") as fp:
			for line in buf:
				fp.write(line)
				fp.write("\n")
			ret = FAIL

	return ret


def main(argv: Optional[Sequence[str]] = None) -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument('filenames', nargs='*', help='Filenames to fix')
	args = parser.parse_args(argv)

	retv = PASS

	for arg in args.filenames:
		ret_for_file = fix_requirements(arg)

		if ret_for_file:
			print(f'Sorting {arg}')

		retv |= ret_for_file

	return retv


if __name__ == '__main__':  # pragma: no cover
	exit(main())

# stdlib
from typing import List, Tuple

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from packaging.requirements import InvalidRequirement
from packaging.requirements import Requirement as _Requirement

__all__ = ["Requirement", "read_requirements", "FAIL", "PASS"]

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

	def __hash__(self) -> int:
		return hash((self.name, self.url, tuple(self.extras), tuple(self.specifier), self.marker))


def read_requirements(req_file: PathLike) -> Tuple[List[Requirement], List[str], List[str]]:

	req_file = PathPlus(req_file)

	comments = []
	invalid_lines: List[str] = []
	requirements: List[Requirement] = []

	for line in req_file.read_text().split("\n"):
		if line.startswith("#"):
			comments.append(line)
		elif line:
			try:
				req = Requirement(line)
				if req.name.lower() not in [r.name.lower() for r in requirements]:
					requirements.append(req)
			except InvalidRequirement:
				invalid_lines.append(line)

	return requirements, invalid_lines, comments

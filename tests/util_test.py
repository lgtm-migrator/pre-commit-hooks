# this package
from pre_commit_hooks.util import Requirement


def test_requirement_object():
	assert Requirement("foo") != Requirement("bar")
	assert Requirement("foo") == Requirement("foo")
	assert Requirement("foo>=1.2.3") == Requirement("foo >= 1.2.3")

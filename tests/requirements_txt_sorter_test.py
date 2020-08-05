# 3rd party
import pytest

# this package
from pre_commit_hooks.requirements_txt_sorter import FAIL, PASS, Requirement, main


@pytest.mark.parametrize(
		('input_s', 'expected_retval', 'output'),
		(
				('', PASS, ''),
				('\n', PASS, '\n'),
				('# intentionally empty\n', PASS, '# intentionally empty\n'),
				('foo\n# comment at end\n', PASS, 'foo\n# comment at end\n'),
				('foo\nbar\n', FAIL, 'bar\nfoo\n'),
				('bar\nfoo\n', PASS, 'bar\nfoo\n'),
				('a\nc\nb\n', FAIL, 'a\nb\nc\n'),
				# ('a\nc\n', FAIL, 'a\nb\nc\n'),
				('a\nb\nc', FAIL, 'a\nb\nc\n'),
				(
						'#comment1\nfoo\n#comment2\nbar\n',
						FAIL,
						'#comment1\n#comment2\nbar\nfoo\n',
						),
				(
						'#comment1\nbar\n#comment2\nfoo\n',
						PASS,
						'#comment1\nbar\n#comment2\nfoo\n',
						),
				('#comment\n\nfoo\nbar\n', FAIL, '#comment\nbar\nfoo\n'),
				('#comment\n\nbar\nfoo\n', PASS, '#comment\n\nbar\nfoo\n'),
				('\nfoo\nbar\n', FAIL, 'bar\nfoo\n'),
				('\nbar\nfoo\n', PASS, '\nbar\nfoo\n'),
				(
						'pyramid-foo==1\npyramid>=2\n',
						FAIL,
						'pyramid>=2\npyramid-foo==1\n',
						),
				(
						'a==1\n'
						'c>=1\n'
						'bbbb!=1\n'
						'c-a>=1;python_version>="3.6"\n'
						'e>=2\n'
						'd>2\n'
						'g<2\n'
						'f<=2\n',
						FAIL,
						'a==1\n'
						'bbbb!=1\n'
						'c>=1\n'
						'c-a>=1; python_version >= "3.6"\n'
						'd>2\n'
						'e>=2\n'
						'f<=2\n'
						'g<2\n',
						),
				('ocflib\nDjango\nPyMySQL\n', FAIL, 'Django\nocflib\nPyMySQL\n'),
				('bar\npkg-resources==0.0.0\nfoo\n', FAIL, 'bar\nfoo\n'),
				('foo\npkg-resources==0.0.0\nbar\n', FAIL, 'bar\nfoo\n'),
				('foo???1.2.3\nbar\n', FAIL, 'bar\n'),
				),
		)
def test_integration(input_s, expected_retval, output, tmpdir):
	path = tmpdir.join('file.txt')
	path.write_text(input_s, encoding="UTF-8")

	output_retval = main([str(path)])

	assert path.read_text(encoding="UTF-8") == output
	assert output_retval == expected_retval


def test_requirement_object():
	assert Requirement("foo") != Requirement("bar")
	assert Requirement("foo") == Requirement("foo")
	assert Requirement("foo>=1.2.3") == Requirement("foo >= 1.2.3")

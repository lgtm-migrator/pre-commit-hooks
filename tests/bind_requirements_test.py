# 3rd party
import pytest

# this package
from pre_commit_hooks.bind_requirements import main
from pre_commit_hooks.util import FAIL, PASS, Requirement


@pytest.mark.parametrize(
		('input_s', 'expected_retval', 'output'),
		(
				('', PASS, ''),
				('\n', PASS, '\n'),
				('# intentionally empty\n', PASS, '# intentionally empty\n'),
				('foo\n# comment at end\n', FAIL, '# comment at end\nfoo>=.1\n'),
				('foo\nbar\n', FAIL, 'bar>=0.2.1\nfoo>=.1\n'),
				('bar\nfoo\n', FAIL, 'bar>=0.2.1\nfoo>=.1\n'),
				('a\nc\nb\n', FAIL, 'a>=1.0\nb>=1.0.0\nc>=0.1.0\n'),
				('a\nb\nc', FAIL, 'a>=1.0\nb>=1.0.0\nc>=0.1.0\n'),
				(
						'#comment1\nfoo\n#comment2\nbar\n',
						FAIL,
						'#comment1\n#comment2\nbar>=0.2.1\nfoo>=.1\n',
						),
				(
						'#comment1\nbar\n#comment2\nfoo\n',
						FAIL,
						'#comment1\n#comment2\nbar>=0.2.1\nfoo>=.1\n',
						),
				('#comment\n\nfoo\nbar\n', FAIL, '#comment\nbar>=0.2.1\nfoo>=.1\n'),
				('#comment\n\nbar\nfoo\n', FAIL, '#comment\nbar>=0.2.1\nfoo>=.1\n'),
				('\nfoo\nbar\n', FAIL, 'bar>=0.2.1\nfoo>=.1\n'),
				('\nbar\nfoo\n', FAIL, 'bar>=0.2.1\nfoo>=.1\n'),
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
				('ocflib\nDjango\nPyMySQL\n', FAIL, 'Django>=3.1.3\nocflib>=2020.10.9.8.6\nPyMySQL>=0.10.1\n'),
				('bar\npkg-resources==0.0.0\nfoo\n', FAIL, 'bar>=0.2.1\nfoo>=.1\npkg-resources==0.0.0\n'),
				('foo\npkg-resources==0.0.0\nbar\n', FAIL, 'bar>=0.2.1\nfoo>=.1\npkg-resources==0.0.0\n'),
				('foo???1.2.3\nbar\n', FAIL, 'foo???1.2.3\nbar>=0.2.1\n'),
				),
		)
def test_integration(input_s, expected_retval, output, tmpdir):
	path = tmpdir.join('file.txt')
	path.write_text(input_s, encoding="UTF-8")

	output_retval = main([str(path)])

	assert path.read_text(encoding="UTF-8") == output
	assert output_retval == expected_retval

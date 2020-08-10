#################
pre-commit-hooks
#################

.. start short_desc

**Some useful hooks for pre-commit.**

.. end short_desc

Well, there's only one at the minute.

See also: https://github.com/pre-commit/pre-commit

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor|
	
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|



.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/pre-commit-hooks/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/pre-commit-hooks
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/pre-commit-hooks/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/pre-commit-hooks/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/pre-commit-hooks/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/pre-commit-hooks/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/pre-commit-hooks/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/pre-commit-hooks/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/pre-commit-hooks/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/pre-commit-hooks?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/pre-commit-hooks?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/pre-commit-hooks
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/pre-commit-hooks
	:target: https://pypi.org/project/pre-commit-hooks/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pre-commit-hooks?logo=python&logoColor=white
	:target: https://pypi.org/project/pre-commit-hooks/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pre-commit-hooks
	:target: https://pypi.org/project/pre-commit-hooks/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/pre-commit-hooks
	:target: https://pypi.org/project/pre-commit-hooks/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/pre-commit-hooks
	:target: https://github.com/domdfcoding/pre-commit-hooks/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/pre-commit-hooks
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/pre-commit-hooks/v0.0.2
	:target: https://github.com/domdfcoding/pre-commit-hooks/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/pre-commit-hooks
	:target: https://github.com/domdfcoding/pre-commit-hooks/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. end shields

Using pre-commit-hooks with pre-commit
---------------------------------------

Add this to your `.pre-commit-config.yaml`

.. code-block:: yaml

	-   repo: https://github.com/domdfcoding/pre-commit-hooks
	    rev: v0.0.2  # Use the ref you want to point at
	    hooks:
	    -   id: requirements-txt-sorter
	    # -   id: ...

Hooks available
-----------------

``requirements-txt-sorter``
Sorts `PEP508 <https://www.python.org/dev/peps/pep-0508/>`_ entries in requirements.txt and removes invalid entries, including ``pkg-resources==0.0.2``.

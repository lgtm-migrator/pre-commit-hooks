#################
pre_commit_hooks
#################

.. start short_desc

**Some useful hooks for pre-commit.**

.. end short_desc

See also: https://github.com/pre-commit/pre-commit

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor|

	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/pre_commit_hooks/latest?logo=read-the-docs
	:target: https://pre_commit_hooks.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |docs_check| image:: https://github.com/domdfcoding/pre_commit_hooks/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/pre_commit_hooks/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/pre_commit_hooks/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/pre_commit_hooks
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/pre_commit_hooks/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/pre_commit_hooks/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/pre_commit_hooks/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/pre_commit_hooks/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/pre_commit_hooks/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/pre_commit_hooks/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/pre_commit_hooks/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/pre_commit_hooks?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/pre_commit_hooks?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/pre_commit_hooks
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/pre_commit_hooks
	:target: https://pypi.org/project/pre_commit_hooks/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pre_commit_hooks?logo=python&logoColor=white
	:target: https://pypi.org/project/pre_commit_hooks/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pre_commit_hooks
	:target: https://pypi.org/project/pre_commit_hooks/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/pre_commit_hooks
	:target: https://pypi.org/project/pre_commit_hooks/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/pre_commit_hooks
	:target: https://github.com/domdfcoding/pre_commit_hooks/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/pre_commit_hooks
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/pre_commit_hooks/v0.0.0
	:target: https://github.com/domdfcoding/pre_commit_hooks/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/pre_commit_hooks
	:target: https://github.com/domdfcoding/pre_commit_hooks/commit/master
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
	    rev: v0.0.0  # Use the ref you want to point at
	    hooks:
	    -   id: requirements-txt-sorter
	    # -   id: ...

Hooks available
-----------------

``requirements-txt-sorter``
Sorts `PEP508 <https://www.python.org/dev/peps/pep-0508/>`_ entries in requirements.txt and removes invalid entries, including ``pkg-resources==0.0.0``.

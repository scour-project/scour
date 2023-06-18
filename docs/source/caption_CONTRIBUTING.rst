.. _contributing-reference-label:

Contributing
############

Contributions to Scour are welcome, feel free to create a pull request (PR)!

In order to be able to merge your PR as fast as possible please try to stick to the following guidelines.

.. important::
    Always run `make check <https://github.com/scour-project/scour/blob/master/Makefile>`_
    before creating a PR to check for common problems.

Code Style
~~~~~~~~~~

The Scour project tries to follow the coding conventions described in
`PEP 8 - The Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/)>`_.
While there are some inconsistencies in existing code
(e.g. with respect to naming conventions and the usage of globals), new code should always abide by the standard.

To quickly check for common mistakes you can use `flake8 <https://pypi.python.org/pypi/flake8>`_.
Our `Makefile <https://github.com/scour-project/scour/blob/master/Makefile>`_
has a convenience target with the correct options:

.. raw:: html

   <details>
   <summary><a>Makefile description</a></summary>
   <br>

The file `Makefile` in the root of the project is used to instruct the *make* tool.
*make* is a well known tool in C or C++. It is also useful in Python to define a set of actions (rules).
A rule has three parts. A target (name), a list of prerequisites, and a recipe (shell commands).

.. code-block:: makefile

    check: test flake8


Target is *check*. No recipe.
Prerequisites list is *test flake8*. *test* and *flake8* are targets in the Makefile.


.. code-block:: makefile

    test:
        python test_scour.py

Target is *test* with no prerequisites. Recipe is *python test_scour.py*.

.. raw:: html

   </details>
   <br>

Makefile command::

	make flake8


Unit Tests
~~~~~~~~~~

In order to check functionality of Scour and prevent any regressions in existing code a number of tests exist which use the 
`unittest <https://docs.python.org/library/unittest.html>`_ unit testing framework which ships with Python. 
You can quickly run the tests by using the `Makefile <https://github.com/scour-project/scour/blob/master/Makefile>`_ convenience target:

Makefile::

	make test

These tests are run automatically on all PRs using `TravisCI <https://travis-ci.org/scour-project/scour>`_ 
and have to pass at all times! When you add new functionality you should always include suitable tests 
with your PR (see `test_scour.py <https://github.com/scour-project/scour/blob/master/test_scour.py>`_)

Coverage
~~~~~~~~

To ensure that all possible code conditions are covered by a test you can use `coverage <https://pypi.python.org/pypi/coverage>`_. 
The `Makefile <https://github.com/scour-project/scour/blob/master/Makefile>`_ convenience target automatically creates an HTML report in `htmlcov/index.html`:

Makefile::

	make coverage

These reports are also created automatically by our TravisCI builds and are accessible via `Codecov <https://codecov.io/gh/scour-project/scour>`_


Pull request
~~~~~~~~~~~~

Feel free to create an issue (button) with a description for the PR and the PR number.
An issue makes it more likely that the PR is recognized in time.

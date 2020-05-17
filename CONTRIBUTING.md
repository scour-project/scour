# Contributing

Contributions to Scour are welcome, feel free to create a pull request!

In order to be able to merge your PR as fast as possible please try to stick to the following guidelines.

> _**TL;DR** (if you now what you're doing) –  Always run [`make check`](https://github.com/scour-project/scour/blob/master/Makefile) before creating a PR to check for common problems._


## Code Style

The Scour project tries to follow the coding conventions described in [PEP 8 - The Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/). While there are some inconsistencies in existing code (e.g. with respect to naming conventions and the usage of globals), new code should always abide by the standard.

To quickly check for common mistakes you can use [`flake8`](https://pypi.python.org/pypi/flake8). Our [Makefile](https://github.com/scour-project/scour/blob/master/Makefile) has a convenience target with the correct options:
```Makefile
make flake8
```

## Unit Tests

In order to check functionality of Scour and prevent any regressions in existing code a number of tests exist which use the [`unittest`](https://docs.python.org/library/unittest.html) unit testing framework which ships with Python. You can quickly run the tests by using the [Makefile](https://github.com/scour-project/scour/blob/master/Makefile) convenience target:
```Makefile
make test
```

These tests are run automatically on all PRs using [TravisCI](https://travis-ci.org/scour-project/scour) and have to pass at all times! When you add new functionality you should always include suitable tests with your PR (see [`test_scour.py`](https://github.com/scour-project/scour/blob/master/test_scour.py)).

### Coverage

To ensure that all possible code conditions are covered by a test you can use [`coverage`](https://pypi.python.org/pypi/coverage). The [Makefile](https://github.com/scour-project/scour/blob/master/Makefile) convenience target automatically creates an HTML report in `htmlcov/index.html`:
```Makefile
make coverage
```

These reports are also created automatically by our TravisCI builds and are accessible via [Codecov](https://codecov.io/gh/scour-project/scour)
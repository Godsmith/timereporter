def pytest_ignore_collect(path, config):
    # Ignore setup.py when running pytest with doctest.
    # Will be fixed in the next pytest release, see
    # https://bitbucket.org/pytest-dev/pytest/issues/502
    return 'setup.py' in str(path)

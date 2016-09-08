import json

import pytest
from jsonschema import ValidationError, validate

from comment import create_app
from comment.configs import settings as app_settings


class MonkeyPatchWrapper(object):
    def __init__(self, monkeypatch, wrapped_object):
        super(MonkeyPatchWrapper, self).__setattr__('monkeypatch', monkeypatch)
        super(MonkeyPatchWrapper, self).__setattr__('wrapped_object',
                                                    wrapped_object)

    def __getattr__(self, attr):
        return getattr(self.wrapped_object, attr)

    def __setattr__(self, attr, value):
        self.monkeypatch.setattr(self.wrapped_object, attr, value,
                                 raising=False)

    def __delattr__(self, attr):
        self.monkeypatch.delattr(self.wrapped_object, attr)


@pytest.fixture
def settings(monkeypatch):
    return MonkeyPatchWrapper(monkeypatch, app_settings)


@pytest.fixture
def json_dumps():
    return json.dumps


@pytest.fixture
def json_loads():
    return json.loads


@pytest.fixture
def cli(loop, test_client, monkeypatch):
    monkeypatch.setattr('aiohttp_autoreload.start', lambda: None)
    return loop.run_until_complete(test_client(create_app))


@pytest.fixture
def json_valid():
    def valid(_json, schema):
        try:
            validate(_json, schema)
            return True
        except ValidationError as e:
            return str(e),

    return valid


@pytest.yield_fixture
def file_open():
    file = None

    def opener(filename, mode):
        nonlocal file
        assert file is None
        file = open(filename, mode)
        return file

    yield opener

    if file is not None:
        file.close()

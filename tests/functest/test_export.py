import os
from urllib.parse import urlparse

import pytest


@pytest.mark.parametrize('_format', ('json', 'xml'))
async def test_comments_export(_format, cli, settings, file_open):
    resp = await cli.get('/comments/users/1/export.{}'.format(_format))
    path = os.path.join(settings.MEDIA_ROOT, urlparse(resp.url).path.replace(settings.MEDIA_URL, ''))
    assert await resp.text() == file_open(path, 'r').read()

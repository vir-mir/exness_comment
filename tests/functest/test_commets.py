import pytest


@pytest.mark.parametrize('data', (
        {"user_id": 1, "entity_id": 1, "parent_id": 0, "text": "test"},
        {"user_id": 1, "entity_id": 1, "parent_id": 0, "text": "test"},
        {"user_id": 1, "entity_id": 1, "parent_id": 1, "text": "test"},
        {"user_id": 1, "entity_id": 1, "parent_id": 1, "text": "test"},
))
async def test_create_comment(data, cli, json_dumps, json_valid, schema_comment):
    resp = await cli.post('/comments', data=json_dumps(data))
    assert resp.status == 201
    assert json_valid(await resp.json(), schema_comment) is True


@pytest.mark.parametrize('data', (
        {'first_level': 1, 'limit': 1, 'page': 1, 'entity_id': 1},
        {'first_level': 1, 'limit': 1, 'page': 2, 'entity_id': 1},
))
async def test_comments_firs_level(data, cli, json_valid, schema_comments):
    resp = await cli.get('/comments', params=data)
    assert resp.status == 200
    assert json_valid(await resp.json(), schema_comments(max_item=1, min_item=1)) is True


async def test_comments_parent(cli, json_valid, schema_comments):
    resp = await cli.get('/comments', params={'parent_id': 1, 'entity_id': 1})
    assert resp.status == 200
    assert json_valid(await resp.json(), schema_comments(max_item=1, min_item=1, parent=True)) is True


async def test_comments_entity(cli, json_valid, schema_comments):
    resp = await cli.get('/comments', params={'entity_id': 1})
    assert resp.status == 200
    assert json_valid(await resp.json(), schema_comments(min_item=1, parent=True)) is True


@pytest.mark.parametrize('id_comment,status,is_json', (
        (1, 202, True),
        (999999, 406, {'message': 'not comment id 999999'}),
))
async def test_comment_edit_by_id(id_comment, status, is_json, cli, json_dumps, json_valid, schema_comment):
    resp = await cli.put('/comments/{}'.format(id_comment), data=json_dumps({"text": "Проверка"}))
    assert resp.status == status

    if is_json is True:
        assert json_valid(await resp.json(), schema_comment) is True
    else:
        assert await resp.json() == {'message': 'not comment id 999999'}


async def test_comments_users(cli, json_valid, schema_comments):
    resp = await cli.get('/comments/users/1')
    assert resp.status == 200
    assert json_valid(await resp.json(), schema_comments(min_item=1)) is True


async def test_comments_history(cli, json_valid, schema_comments_history):
    resp = await cli.get('/comments/history/1')
    assert resp.status == 200
    assert json_valid(await resp.json(), schema_comments_history) is True

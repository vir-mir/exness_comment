async def test_create_entities(cli, json_dumps):
    resp = await cli.post('/entities', data=json_dumps({
        'name': 'Проверка'
    }))
    assert resp.status == 201


async def test_get_entities(cli, json_valid):
    resp = await cli.get('/entities')
    assert resp.status == 200
    json = await resp.json()
    schema = {
        'type': 'array',
        'minItem': 1,
        'items': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                "id": {'type': 'integer'},
            },
            'required': ['id', 'name']
        }
    }

    assert json_valid(json, schema) is True

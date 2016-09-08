async def test_main(cli):
    resp = await cli.get('/')
    assert resp.status == 404
    assert await resp.json() == {"message": "Not Found"}

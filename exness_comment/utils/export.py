from xml.etree import ElementTree as et

from .views import dumps


async def export_json(data):
    return dumps(list(map(dict, await data.fetchall()))).encode()


async def export_xml(data):
    root = et.Element('comments')
    async for comment in data:
        comment = dict(comment)
        comment_node = et.SubElement(root, 'comment', comment_id=str(comment['id']))

        for key, val in comment.items():
            node = et.SubElement(comment_node, key)
            node.text = str(val)
    xml = '<?xml version="1.0" encoding="utf-8"?>\n{}'.format(et.tostring(root).decode())

    return xml.encode()


def factory_export(func):
    methods = {
        'json': export_json,
        'xml': export_xml
    }

    return methods[func]

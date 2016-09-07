import uuid

import sqlalchemy as sa

from .db import Transaction


async def delete_tree(table, conn, pk):
    query = (sa.select([table])
             .select_from(table)
             .where(table.id == pk))

    async with Transaction(conn) as conn:
        comment = await (await conn.execute(query)).fetchone()

        if comment is None:
            return 'not comment id %s' % pk

        query = (sa.select([table.id])
                 .select_from(table)
                 .where(table.parent_id == pk))

        if (await conn.execute(query)).rowcount > 0:
            return 'in %s comments have children' % pk

        query = sa.delete(table).where(table.id == pk)
        await conn.execute(query)

        query = (sa.update(table)
                 .values(rkey=(table.rkey - (comment.rkey - comment.lkey + 1)))
                 .where(sa.and_(table.rkey > comment.rkey,
                                table.lkey < comment.lkey,
                                table.tree_id == comment.tree_id)))

        await conn.execute(query)

        return dict(comment)


async def insert_tree(table, conn, parent_id, data: dict = None):
    data = data or {}

    query = (sa.select([table.rkey, table.lkey, table.level, table.tree_id])
             .select_from(table)
             .where(table.id == parent_id))
    async with Transaction(conn) as conn:
        parent_comment = await (await conn.execute(query)).fetchone()

        if parent_comment is None:
            lkey = 0
            rkey = 1
            level = 0
            parent_id = None
            tree_id = uuid.uuid4().hex
        else:
            lkey = parent_comment.rkey
            rkey = parent_comment.rkey + 1
            level = parent_comment.level + 1
            tree_id = parent_comment.tree_id

            query = (sa.update(table)
                     .values(rkey=table.rkey + 2,
                             lkey=sa.case([(table.lkey > parent_comment.rkey, table.lkey + 2)], else_=table.lkey))
                     .where(sa.and_(table.rkey >= parent_comment.rkey, table.tree_id == tree_id)))

            await conn.execute(query)

        values = {
            'level': level,
            'rkey': rkey,
            'lkey': lkey,
            'parent_id': parent_id,
            'tree_id': tree_id,
        }
        values.update(data)
        query = sa.insert(table).values(**values).return_defaults()
        return await conn.execute(query)

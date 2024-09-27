import os.path

from sqlalchemy import select

from models.model import ListRecipes, Recipes
from tests.conftest import async_session


async def test_start(db_client):
    res = os.path.exists("test_recipes.db")
    async with async_session() as session:
        qr_rec: [Recipes] = await session.execute(select(Recipes))
        res_recipes: [Recipes] = qr_rec.scalars().all()

        qr_list_rec: [ListRecipes] = await session.execute(select(ListRecipes))
        res_llist_rec: [ListRecipes] = qr_list_rec.scalars().all()

    assert len(res_recipes) == 10
    assert len(res_llist_rec) == 10
    assert res

import os
from random import choice, randint

from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from models.database import Base
from models.model import ListRecipes, Recipes

test_db_url = "sqlite+aiosqlite:///test_recipes.db"

engine = create_async_engine(test_db_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@fixture
async def db_client():
    # asyncio.run(main())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    name = [
        "Жаркое",
        "Суп",
        "Жареная картошка",
        "Макароны",
        "Запеканка",
        "Омлет",
        "Овсяная каша с фруктами",
        "Шашлык",
        "Борщ",
        "Плов",
        "Компот",
        "Запеканка",
        "Торт",
        "Гречневая каша с тушенкой",
        "Овощной салат",
        "Перловая каша",
        "Лазанья",
        "Винегрет",
    ]
    ingredients = [
        "лук",
        "морковка",
        "макароны",
        "свинина",
        "картофель",
        "огурцы",
        "помидоры",
        "болгарский перец",
        "яблоки",
        "бананы",
        "апельсины",
        "сливочное масло",
        "соль",
        "специи",
        "чеснок",
        "сахар",
        "варенье",
        "мята",
        "свекла",
        "молоко",
        "сок",
        "кабачки",
        "тыква",
        "арахис",
        "грецкий орех",
        "изюм",
        "гречка",
        "рис",
        "овсяная крупа",
        "горох",
        "яйца",
        "кофе",
        "чай",
        "абрикос",
        "персик",
        "арбуз",
    ]
    description = [
        "все порезать посолить",
        "варить 30 минут",
        "жарить на медленном огне",
        "резать мелкими кубиками",
        "помыть",
        "добавить по вкусу",
        "запекать в духовке",
        "температура 200 градусов",
        "достать из холодильника",
        "потрясти перед применением",
        "резать полосками",
        "варить до полной готовности",
    ]
    rec_list: list = [
        Recipes(
            name=choice(name),
            ingredients={choice(ingredients): f"{randint(1, n + 1)} шт" for n in range(randint(1, 5))},
            description=",".join([choice(description) for l in range(3)]),
            some_inf=ListRecipes(),
        )
        for _ in range(10)
    ]
    async with async_session() as session:
        session.add_all(rec_list)
        await session.commit()
        print(rec_list)
    yield
    os.remove("test_recipes.db")

from random import randint

from sqlalchemy import Column, ForeignKey, PickleType
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base


class Recipes(Base):
    __tablename__ = "Recipes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    # не нашел способ как записывать в БД словарь или список, в том числе хотелось бы записать через mapped_column
    ingredients = Column(PickleType, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    some_inf: Mapped["ListRecipes"] = relationship(back_populates="recipe", cascade="all, delete-orphan")

    def __repr__(self):
        return "".join([str(getattr(self, c.name)) + " - " for c in self.__table__.columns])


class ListRecipes(Base):
    __tablename__ = "ListRecipes"
    name: Mapped[int] = mapped_column(ForeignKey("Recipes.id"), primary_key=True)
    views: Mapped[int] = mapped_column(nullable=False, default=0)
    cooking_time: Mapped[str] = mapped_column(default=f"{randint(30, 120)} минут")
    recipe: Mapped["Recipes"] = relationship(back_populates="some_inf")

    def __repr__(self):
        return "".join([str(getattr(self, c.name)) + " - " for c in self.__table__.columns])


#
# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     name = [
#         "Жаркое",
#         "Суп",
#         "Жареная картошка",
#         "Макароны",
#         "Запеканка",
#         "Омлет",
#         "Овсяная каша с фруктами",
#         "Шашлык",
#         "Борщ",
#         "Плов",
#         "Компот",
#         "Запеканка",
#         "Торт",
#         "Гречневая каша с тушенкой",
#         "Овощной салат",
#         "Перловая каша",
#         "Лазанья",
#         "Винегрет",
#     ]
#     ingredients = [
#         "лук",
#         "морковка",
#         "макароны",
#         "свинина",
#         "картофель",
#         "огурцы",
#         "помидоры",
#         "болгарский перец",
#         "яблоки",
#         "бананы",
#         "апельсины",
#         "сливочное масло",
#         "соль",
#         "специи",
#         "чеснок",
#         "сахар",
#         "варенье",
#         "мята",
#         "свекла",
#         "молоко",
#         "сок",
#         "кабачки",
#         "тыква",
#         "арахис",
#         "грецкий орех",
#         "изюм",
#         "гречка",
#         "рис",
#         "овсяная крупа",
#         "горох",
#         "яйца",
#         "кофе",
#         "чай",
#         "абрикос",
#         "персик",
#         "арбуз",
#     ]
#     description = [
#         "все порезать посолить",
#         "варить 30 минут",
#         "жарить на медленном огне",
#         "резать мелкими кубиками",
#         "помыть",
#         "добавить по вкусу",
#         "запекать в духовке",
#         "температура 200 градусов",
#         "достать из холодильника",
#         "потрясти перед применением",
#         "резать полосками",
#         "варить до полной готовности",
#     ]
#     rec_list: list = [
#         Recipes(
#             name=choice(name),
#             ingredients={choice(ingredients): f"{randint(1, n + 1)} шт" for n in range(randint(1, 5))},
#             description=",".join([choice(description) for l in range(3)]),
#             some_inf=ListRecipes(),
#         )
#         for _ in range(10)
#     ]
#     async with async_session() as session:
#         session.add_all(rec_list)
#         await session.commit()
#         print(rec_list)
#
#
# async def add_recipe(some_recipe: Recipes, async_sess: async_sessionmaker):
#     async with async_sess() as session:
#         session.add(some_recipe)
#         # await session.flush()
#         await session.commit()
#         print(some_recipe)
#         print(some_recipe.some_inf)
#
#
# async def get_recipe(some_recipe_id: int, async_sess: async_sessionmaker):
#     async with async_sess() as session:
#         qr: [Recipes] = await session.execute(
#             select(Recipes).where(Recipes.id == some_recipe_id).options(selectinload(Recipes.some_inf))
#         )
#         res: Recipes = qr.scalars().one_or_none()
#         if res:
#             res.some_inf.views += 1
#             print(res.some_inf)
#             await session.commit()
#
#
# async def main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     await init_db()
#     d = Recipes(
#         name="Название рецепта",
#         ingredients={"prod1": "1 pc", "prod2": "2 pc"},
#         description="some discr",
#         some_inf=ListRecipes(),
#     )
#     await add_recipe(d, async_session)
#     await get_recipe(1, async_session)


# if __name__ == "__main__":
# asyncio.run(main())

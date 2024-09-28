from random import choice, randint

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.database import Base, async_session, engine
from models.model import ListRecipes, Recipes
from models.utilits.schemas import ListRecipesModel, RecipesIn, RecipesOut

app = FastAPI()


@app.on_event("startup")
async def shutdown():
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


@app.on_event("shutdown")
async def shutdown():
    await async_session.close()
    await engine.dispose()


@app.get("/")
async def hello():
    return {"hello": "world"}


@app.get("/recipes/{id}", response_model=RecipesOut)
async def get_recipes_id(id: int) -> Recipes:
    async with async_session() as session:
        qr: [Recipes] = await session.execute(
            select(Recipes).where(Recipes.id == id).options(selectinload(Recipes.some_inf))
        )
        res: Recipes = qr.scalars().one_or_none()
        print(res)
        if res:
            res.some_inf.views += 1
            print(res.some_inf)
            await session.commit()
            return res
        else:
            raise HTTPException(status_code=404, detail="Item not found")


@app.post("/recipes", response_model=RecipesOut)
async def add_recipes(some_recipe: RecipesIn, some_list_recipe: ListRecipesModel):
    new_list = ListRecipes(**some_list_recipe.model_dump())
    new_recipe = Recipes(**some_recipe.model_dump())
    new_recipe.some_inf = new_list
    async with async_session() as session:
        session.add(new_recipe)
        await session.commit()

        return new_recipe


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

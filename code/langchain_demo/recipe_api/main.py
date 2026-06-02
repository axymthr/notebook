from fastapi import FastAPI, Query
from recipe import get_recipe

app = FastAPI()

@app.get("/")
def get_recipe_text(
    cuisine: str = Query(),
    mealtime: str = Query()
):
    result = get_recipe(
         cuisine,
         mealtime
    )
    return result

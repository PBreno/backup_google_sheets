from fastapi import FastAPI
from sheets import sheet, driver
app = FastAPI()

app.include_router(sheet.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

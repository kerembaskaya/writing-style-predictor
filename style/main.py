from fastapi import FastAPI

app = FastAPI()


@app.get("/style")
async def root():
    return {"message": "Hello World"}

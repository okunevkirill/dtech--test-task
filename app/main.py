from fastapi import FastAPI

app = FastAPI(
    title="dtech--test-task",
)


@app.get("/")
async def root():
    return {"message": "It's a live..."}

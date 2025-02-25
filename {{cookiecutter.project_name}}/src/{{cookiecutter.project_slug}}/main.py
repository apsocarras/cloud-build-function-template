from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the {{cookiecutter.project_name}} project!"}

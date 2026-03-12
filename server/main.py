from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users")
def list_users():
    return ["ofer", "maya", "avi", "dana"]


@app.post("/users")
def create_user():
    pass

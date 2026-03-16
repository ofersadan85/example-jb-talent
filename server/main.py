from pathlib import Path

from fastapi import FastAPI, Request
from models import User

app = FastAPI()
app.state.count = 0
DEFAULT_USERS_DIR = Path(__file__).parent / "users"


@app.get("/count")
async def count(request: Request) -> int:
    request.app.state.count += 1
    return request.app.state.count


@app.get("/users")
async def list_users() -> list[User]:
    return [User.model_validate_json(f.read_text()) for f in DEFAULT_USERS_DIR.glob("*.json")]


@app.get("/users/{id}")
async def get_user(id: int) -> User:
    return User.load_from_file(DEFAULT_USERS_DIR, id)


@app.get("/users/{id}/{field_name}")
async def get_user_email(id: int, field_name: str) -> str:
    return User.load_from_file(DEFAULT_USERS_DIR, id).model_dump()[field_name]

from fastapi import FastAPI
from models import User
from pathlib import Path

app = FastAPI()
DEFAULT_USERS_DIR = Path(__file__).parent / "users"


@app.get("/users")
def list_users() -> list[User]:
    return [User.model_validate_json(f.read_text()) for f in DEFAULT_USERS_DIR.glob("*.json")]


@app.get("/user")
def get_user(id: int) -> User:
    return User.load_from_file(DEFAULT_USERS_DIR, id)

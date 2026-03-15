from pathlib import Path
from threading import Thread

import httpx
from pydantic import BaseModel

USERS_URL_PATH = "/users/"
USERS_FULL_URL = "https://jsonplaceholder.typicode.com/" + USERS_URL_PATH


class UserAddress(BaseModel):
    street: str
    city: str


class UserCompany(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class FetchUserIdThread(Thread):
    def __init__(self, id: int, client: httpx.Client | None = None) -> None:
        super().__init__()
        self.id = id
        self.client = client
        self.result = None
        self.start()

    def run(self):
        self.result = User.get_from_web(self.id, self.client)


class User(BaseModel):
    id: int | None
    name: str
    username: str
    email: str
    company: UserCompany | None = None
    address: UserAddress | None = None

    def save_to_file(self, users_dir: Path):
        file_path = users_dir / (str(self.id) + ".json")
        file_path.write_text(self.model_dump_json(indent=2))

    def save_to_web(self, client: httpx.Client | None = None) -> "User":
        user_dump = self.model_dump(exclude={"id"}, exclude_none=True)
        if client is None:
            response = httpx.post(USERS_FULL_URL, json=user_dump)
        else:
            response = client.post(USERS_URL_PATH, json=user_dump)
        return User.model_validate(response.json())

    @classmethod
    def load_from_file(cls, users_dir: Path, id: int) -> "User":
        file_path = users_dir / (str(id) + ".json")
        data = file_path.read_text()
        return cls.model_validate_json(data)

    @classmethod
    def get_from_web(cls, id: int, client: httpx.Client | None = None) -> "User":
        if client is None:
            response = httpx.get(USERS_FULL_URL + str(id))
        else:
            response = client.get(USERS_URL_PATH + str(id))
        return cls.model_validate(response.json())

    @classmethod
    def get_multiple_from_web(
        cls, ids: list[int] | None = None, client: httpx.Client | None = None
    ) -> list["User"]:
        if ids is None:
            if client is None:
                response = httpx.get(USERS_FULL_URL)
            else:
                response = client.get(USERS_URL_PATH)
            return [cls.model_validate(u) for u in response.json()]
        else:
            threads = [FetchUserIdThread(i, client) for i in ids]
            for t in threads:
                t.join()
            return [t.result for t in threads if t.result is not None]

import asyncio
from pathlib import Path

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

    async def save_to_web(self, client: httpx.AsyncClient | None = None) -> "User":
        user_dump = self.model_dump(exclude={"id"}, exclude_none=True)
        if client is None:
            response = httpx.post(USERS_FULL_URL, json=user_dump)
        else:
            response = await client.post(USERS_URL_PATH, json=user_dump)
        return User.model_validate(response.json())

    @classmethod
    def load_from_file(cls, users_dir: Path, id: int) -> "User":
        file_path = users_dir / (str(id) + ".json")
        data = file_path.read_text()
        return cls.model_validate_json(data)

    @classmethod
    async def get_from_web(cls, id: int, client: httpx.AsyncClient | None = None) -> "User":
        if id == 7:
            raise ValueError("WE DONT LIKE SEVEN")
        if client is None:
            response = httpx.get(USERS_FULL_URL + str(id))
        else:
            response = await client.get(USERS_URL_PATH + str(id))
        return cls.model_validate(response.json())

    @classmethod
    async def get_multiple_from_web(
        cls, ids: list[int] | None = None, client: httpx.AsyncClient | None = None
    ) -> list["User"]:
        if ids is None:
            if client is None:
                response = httpx.get(USERS_FULL_URL)
            else:
                response = await client.get(USERS_URL_PATH)
            return [cls.model_validate(u) for u in response.json()]
        else:
            # return [await cls.get_from_web(id, client) for id in ids]  # We won't do this, because it doesn't run in parallel
            inner_tasks = [cls.get_from_web(id, client) for id in ids]
            return await asyncio.gather(*inner_tasks)

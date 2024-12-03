# import os
# from typing import List
import json
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Database(BaseSettings):
    dbms: str
    driver: str
    host: str
    port: int
    user: str
    password: str
    name: str
    charset: str
    echo: bool = False

    def url(self) -> str:
        return f"{self.dbms}+{self.driver}://{self.user}:{self.password}@{self.host}:{str(self.port)}/{self.name}?charset={self.charset}"

    model_config = SettingsConfigDict(env_prefix="DB_")


class Telegram(BaseSettings):
    api_id: str
    api_hash: str
    token: str
    chans_ids: str

    send_chat_id: str
    model_config = SettingsConfigDict(env_prefix="TG_")

    def chans_ids_convert(self) -> list[int]:
        if not isinstance(self.chans_ids, list):
            self.chans_ids = [int(chan) for chan in self.chans_ids.split(",")]
        return self.chans_ids


class Redis(BaseSettings):
    host: str
    port: int
    db: int
    password: str
    # pool_setting = RedisSettings(host=host, port=port, database=db)

    model_config = SettingsConfigDict(env_prefix="RD_")


class Chats(BaseSettings):
    result: dict | None = None

    def __call__(self):
        chats: dict = {}
        with open("chats.json") as j_file:
            chats = json.loads(j_file)
        print(chats)

    def update_data(self):
        chats: dict = {}
        with open("chats.json") as j_file:
            chats = json.load(j_file)
        chats = chats.get("city")
        self.result = chats
        # print(chats)
        return True


class Setting(BaseSettings):
    db: Database = Database()
    tg: Telegram = Telegram()
    redis: Redis = Redis()
    chats: Chats = Chats()


setting = Setting()

if __name__ == "__main__":
    print(setting.tg.api_id)
    print(setting.tg.api_hash)
    print(setting.tg.token)
    print(setting.tg.chans_ids_convert())
    print(setting.redis.host)
    print(setting.chats.update_data())
    print(setting.chats.result)
    print(setting.db.url())

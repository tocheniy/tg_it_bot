# import os
# from typing import List
from dotenv import load_dotenv

# from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


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


class Setting(BaseSettings):
    tg: Telegram = Telegram()


setting = Setting()

if __name__ == "__main__":
    print(setting.tg.api_id)
    print(setting.tg.api_hash)
    print(setting.tg.token)
    print(setting.tg.chans_ids_convert())

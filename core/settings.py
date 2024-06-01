from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    sber: str


@dataclass
class Settings:
    bot: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bot=Bots(
            bot_token=env.str("TOKEN"),
            sber=env.str("SBER_AUTH")
        )
    )


settings = get_settings('input.txt')
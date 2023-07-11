from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    """Read the .env file and return an instance of the Config
        class with the token and admin_ids fields filled in

    Args:
        path: path to the .env file

    Returns: instance of the Config class

    """
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
        token=env('BOT_TOKEN'),
        admin_ids=list(map(int, env.list('ADMIN_IDS')))))

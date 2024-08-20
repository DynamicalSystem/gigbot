from dynamicalsystem.gigbot.commands import _Save, Delete, List, Stash
from dynamicalsystem.gigbot.config import config
from dynamicalsystem.gigbot.storage import RedisStorage, StashStorage
from signalbot import SignalBot, Command, Context

SIGNAL_RPR = config.get("SIGNAL_RPR")
SIGNAL_PHONE_NUMBER = config.get("SIGNAL_PHONE_NUMBER")
REDIS_URL = config.get("REDIS_URL")


def create_signalbot():
    bot = SignalBot(
        {
            "signal_service": SIGNAL_RPR,
            "phone_number": SIGNAL_PHONE_NUMBER,
            "storage": {
                "redis_host": REDIS_URL[7:-5],
                "redis_port": REDIS_URL[-4:],
            },
        }
    )
    bot.storage = RedisStorage(
        bot._redis_host, bot._redis_port
    )  # override the signalbot storage
    bot.stash = StashStorage(
        bot._redis_host, bot._redis_port
    )  # add in a custom stash storage handler
    bot.register(_Save())  # persist all messages to redis
    bot.register(Stash())
    bot.register(List())
    bot.register(Delete())

    return bot

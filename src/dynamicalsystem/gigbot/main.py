from dynamicalsystem.gigbot.config import config
from dynamicalsystem.gigbot.loggers import create_console_logger
from dynamicalsystem.gigbot.signalbot import create_signalbot


def main():
    logger = create_console_logger()
    bot = create_signalbot()
    bot.start()


if __name__ == "__main__":
    main()

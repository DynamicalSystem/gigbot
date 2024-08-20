from dynamicalsystem.gigbot.utils import url_join
from datetime import datetime
from logging import getLogger, Handler, Formatter, StreamHandler, INFO, DEBUG
from requests import post
from sys import stdout


class SignalHandler(Handler):

    def __init__(
        self,
        level: str,
        signal_url: str,
        signal_phone_number: str,
        signal_group_id: str,
    ):
        super().__init__(level)

        self.url = url_join(signal_url, ["v2/send"])

    def emit(self, record):
        headers = {"Content-Type": "application/json"}
        message = self.format(record)
        data = {
            "message": message,
            "number": signal_phone_number,
            "recipients": [signal_group_id],
        }

        response = post(self.url, json=data, headers=headers)
        # TODO: give this access to the console logger
        if not response.ok:
            error = response.json().get("error")
            print("Failed to log to Signal Messenger: %", error.split("\n")[0])

        return response


class SignalFormatter(Formatter):

    def __init__(self, task_name=None):
        super().__init__()

    def format(self, record):
        return (
            f"{record.levelname} "
            f"{record.name}\n"
            f'{datetime.fromtimestamp(record.created).strftime("%d %b %Y, %H:%M:%S")}\n'
            f"{record.msg}"
        )


# TODO: work out why this doesn't show in docker log (although root does)
def create_console_logger(level: str = DEBUG):
    logger = getLogger(__package__)
    logger.setLevel(level)
    handler = StreamHandler(stdout)
    handler.setLevel(level)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.debug("Logger created")

    return logger


# TODO: jang this into the __package__ logger and work out how to trigger it with context
def create_signal_logger(name: str, level: str = "INFO"):
    logging.basicConfig(level=level)
    logger = logging.getLogger(name)
    handler = SignalHandler(level=level)
    formatter = SignalFormatter(logger)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.debug("Logger created")

    return logger

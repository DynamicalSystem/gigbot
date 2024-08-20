from dotenv import dotenv_values
from logging import getLogger, DEBUG
from os import getenv
from os.path import expanduser, join

logger = getLogger(name=f"{__package__}.{__name__}")

CONFIG_FOLDER = getenv("DYNAMICAL_SYSTEM_FOLDER") or exit(
    "DYNAMICAL_SYSTEM_FOLDER not set"
)

if __package__:
    CONFIG_FOLDER = join(CONFIG_FOLDER, __package__, "config")
else:
    exit("Package name not set")

ENVIRONMENT = getenv("DYNAMICAL_SYSTEM_ENVIRONMENT") or exit(
    "DYNAMICAL_SYSTEM_ENVIRONMENT not set"
)
CONFIG_FILE = join(CONFIG_FOLDER, ENVIRONMENT + ".env")
config = dotenv_values(CONFIG_FILE)

# TODO Reinforce validation and create a dot accessible object
# TODO make this a singleton


class Config:
    def __init__(self) -> None:
        self.app_folder = getenv("DYNAMICAL_SYSTEM_FOLDER") or exit(
            "DYNAMICAL_SYSTEM_FOLDER not set"
        )

        if __package__:
            self.config_folder = join(self.app_folder, __package__, "config")
        else:
            exit("Package name not set")

        self.app_environment = getenv("DYNAMICAL_SYSTEM_ENVIRONMENT") or exit(
            "DYNAMICAL_SYSTEM_ENVIRONMENT not set"
        )
        expected_environment_variables = [
            "SIGNAL_RPR",
            "SIGNAL_URL",
            "SIGNAL_LOGGER_GROUP_ID",
            "SIGNAL_PHONE_NUMBER",
            "SIGNAL_SOURCE_UUID",
            "REDIS_URL",
            "REDIS_SERVER",
            "REDIS_PASSWORD",
            "REDIS_CONNECTION_STRING",
            "DYNAMICALSYSTEM_LOG_LEVEL",
        ]

        config_file = join(self.config_folder, self.app_environment + ".env")
        logger.info(f"Loading config from {config_file}")
        config = dotenv_values(config_file)

        for x in expected_environment_variables:
            if x not in config:
                while True:
                    logger.error(f"{x} not found in {config_file}")
                    from time import sleep

                    sleep(20)
                exit(f"{x} not found in {config_file}")
            print(f"{x}: {config[x]}")


validator = Config()

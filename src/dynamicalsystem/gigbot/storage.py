from logging import getLogger
from pickle import dumps, loads
from redis import Redis
from signalbot import Message
from signalbot.storage import Storage, StorageError

logger = getLogger(name=f"{__package__}.{__name__}")


class RedisStorage(Storage):
    def __init__(self, host: str, port: str):
        url = f"redis://default:admin@{host}:{port}/0"
        self._redis = Redis.from_url(url=url)
        logger.info(f"Message store connection established: {url}")

    def exists(self, key: str) -> bool:
        return self._redis.exists(key)

    def read(self, key: str) -> Message:
        try:
            logger.info(f"Load Redis message: {key}")
            return loads(self._redis.get(key))
        except Exception as e:
            raise StorageError(f"Redis message load failed: {e}")

    def save(self, key: str, message: Message):
        try:
            self._redis.set(key, dumps(message))
            logger.info(f"Message saved: {key}")
        except Exception as e:
            logger.exception(f"Redis save message failed: {message}")
            raise StorageError(f"Redis message save failed: {e}")


class StashStorage(Storage):
    def __init__(self, host: str, port: str):
        url = f"redis://default:admin@{host}:{port}"
        self._redis = Redis.from_url(url=url, db=1)
        logger.info(f"Stash connection established:\n{self._redis.info()}")

    def delete(self, key: str):
        try:
            logger.info(f"Deleting redis stash message: {key}")
            return self._redis.delete(key)
        except Exception as e:
            raise StorageError(f"Redis stash delete failed: {e}")

    def exists(self, key: str) -> bool:
        return self._redis.exists(key)

    def read(self, key: str) -> Message:
        try:
            logger.info(f"Loading redis stash message: {key}")
            return loads(self._redis.get(key))
        except Exception as e:
            raise StorageError(f"Redis stash load failed: {e}")

    def read_all(self):
        keys = self._redis.scan_iter(count=100)
        for x in keys:
            yield loads(self._redis.get(x))

    def save(self, key: str, stash: dict):
        try:
            self._redis.set(key, dumps(stash))
            logger.info(f"Stash saved: {key}")
        except Exception as e:
            raise StorageError(f"Redis stash save failed: {e}")

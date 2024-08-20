from base64 import b64encode, decode
from dynamicalsystem.gigbot.config import config
from dynamicalsystem.gigbot.storage import Storage, StorageError
from dynamicalsystem.gigbot.envelopes import (
    reaction_target,
    stash_name,
    reaction_removed,
)
from signalbot import Command, Context
from signalbot.message import Message, MessageType
from pickle import dumps

PHONE_NUMBER = config.get("SIGNAL_PHONE_NUMBER")
SOURCE_UUID = config.get("SIGNAL_SOURCE_UUID")


class _Save(Command):
    # Doesn't handle edits
    async def handle(self, c: Context):
        c.bot.storage.save(c.message.timestamp, c.message)


class Delete(Command):
    commands = ["❌"]

    def describe(self) -> str:
        return "❌: Delete from the stash"

    async def handle(self, c: Context):
        command = (
            c.message.reaction or "_"
        )  # hack to force not None and not empty string

        if any(command in x for x in self.commands):
            if reaction_removed(c.message.raw_message):
                return

            try:
                if target := c.bot.storage.read(
                    key=reaction_target(c.message.raw_message)
                ):
                    key = target.text.split("/n")[0]  # first line of message
                    c.bot.stash.delete(key)
                    target_context = Context(c.bot, target)
                    await target_context.react("🤖")  # TODO wire this up correctly
            except StorageError as e:
                text = f"Johnny Utah! Turn my pages."
                timestamp = await c.send(text)
                sent_message = _sent_message(timestamp, text)
                c.bot.storage.save(timestamp, _sent_message(timestamp, text))


"""
            except Exception as e:
                text = f"Now was I rushing or dragging? {e}"
                timestamp = await c.send(text)
                c.bot.storage.save(timestamp, _sent_message(timestamp, text))
"""


class List(Command):
    commands = ["list", "📋"]

    def describe(self) -> str:
        return "📋|list: List everything in the stash"

    async def handle(self, c: Context):
        command = c.message.text or "_"  # hack to force not None and not empty string

        if any(command in x for x in self.commands):
            for x in c.bot.stash.read_all():
                text = c.bot.storage.read(x).text
                timestamp = await c.send(text)
                sent_message = _sent_message(timestamp, text)
                c.bot.storage.save(timestamp, sent_message)


class Stash(Command):
    commands = ["📌"]

    def describe(self) -> str:
        return "📌: Stash a message for later"

    async def handle(self, c: Context):
        command = (
            c.message.reaction or "_"
        )  # hack to force not None and not empty string

        if any(command in x for x in self.commands):
            try:
                if target := c.bot.storage.read(
                    key=reaction_target(c.message.raw_message)
                ):
                    key = target.text.split("/n")[0]  # first line of message
                    c.bot.stash.save(key, target.timestamp)
                    target_context = Context(c.bot, target)
                    await target_context.react("🤖")
            except StorageError as e:
                text = f"Not quite my tempo."
                timestamp = await c.send(text)
                sent_message = _sent_message(timestamp, text)
                c.bot.storage.save(timestamp, _sent_message(timestamp, text))


def _sent_message(timestamp: int, text: str) -> Message:
    return Message(
        source=PHONE_NUMBER,
        source_number=PHONE_NUMBER,
        source_uuid=SOURCE_UUID,
        timestamp=timestamp,
        type=MessageType.SYNC_MESSAGE,
        text=text,
    )

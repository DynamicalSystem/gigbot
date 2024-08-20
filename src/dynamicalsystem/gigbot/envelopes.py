def reaction_removed(envelope: dict) -> int:
    try:
        return (
            envelope.get("envelope")
            .get("syncMessage")
            .get("sentMessage")
            .get("reaction")
            .get("isRemove")
        )
    except (AttributeError, KeyError, TypeError):
        return None


def reaction_target(envelope: dict) -> int:
    try:
        return (
            envelope.get("envelope")
            .get("syncMessage")
            .get("sentMessage")
            .get("reaction")
            .get("targetSentTimestamp")
        )
    except (AttributeError, KeyError, TypeError):
        return None


def stash_name(envelope: dict) -> str:
    try:
        return envelope.get("envelope").get("dataMessage")["message"].split("/n")[0]
    except (AttributeError, KeyError, TypeError):
        return None

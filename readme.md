# dynamicalsystem.gigbot

`gigbot` listens to Signal groups it's a member of and:

* Stashes a message which gets a 📌 reaction
* Lists the stash when it sees `list`
* Deletes a stashed message which recieves a ❌ reaction from stash

## Setup

This uses a 'src layout' project structure so create a directory structure:

```tree
dynamicalsystem                     <- mkdir this
└── gigbot                          <- you are here
    ├── __init__
    ├── docker-compose.yml
    ├── dockerfile
    ├── makefile
    ├── pyproject.toml
    ├── readme.md
    ├── requirements.txt
    ├── requirements_local.txt
    ├── src
    │   ├── dynamicalsystem         <- namespace
    │   │   └── gigbot
    │   │       ├── __init__
    │   │       ├── commands.py
    │   │       ├── config.py
    │   │       ├── envelopes.py
    │   │       ├── loggers.py
    │   │       ├── main.py
    │   │       ├── signalbot.py
    │   │       ├── storage.py
    │   │       └── utils.py
    └── tests                       <- embarrasingly empty
```

## Configuration

You will need some config files which wire everything up.  I don't keep these on github.

```tree
dynamicalsystem                     <- mkdir this
└── gigbot                          <- clone this
    └── config                      <- mkdir this
        ├── dev.env                 <- create this
        ├── prod.env                <- create this
        └── test.env                <- create this

```

The contents look like the following given the `dockerfile`, `makefile` and `docker-compose.yml` in github:

```bash
# Signal Messenger
SIGNAL_RPR=signal:8010	# The signalbot uses a Relative Path Reference
SIGNAL_URL=http://signal:8010
SIGNAL_LOGGER_GROUP_ID= # The group ID of the Signal chat room you want to log to
SIGNAL_PHONE_NUMBER=+44123456789
SIGNAL_SOURCE_UUID= # The UUID Signal associates with the phone number

# REDIS
REDIS_URL=http://redis:6379
REDIS_SERVER=redis
REDIS_PASSWORD=
REDIS_CONNECTION_STRING=redis://default:${REDIS_PASSWORD}@${REDIS_SERVER}:6379

# App
DYNAMICALSYSTEM_LOG_LEVEL=DEBUG
```

Don't worry about most of this for now... the only required items are the `SIGNAL_PHONE_NUMBER` and the `SIGNAL_SOURCE_UUID`. You need to get Signal up and running which is a whole other thingy.

## Build

```bash
% make deploy ENV=test
```

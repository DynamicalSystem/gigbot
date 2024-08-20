# dynamicalsystem.gigbot

`gigbot` listens to Signal groups it's a member of and:

* Stashes a message which gets a 📌 reaction
* Lists the stash when it sees `list`
* Deletes a stashed message which recieves a ❌ reaction from stash

It uses [https://github.com/filipre/signalbot/](signalbot) by [https://github.com/filipre](filipre) which is just great.  signalbot uses [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) by [https://hub.docker.com/u/bbernhard](bbernhard) which, too, is fab.  There's a `redis` backend which just works.

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

```zsh
gigbot % python -m venv .venv
gigbot % source .venv/bin/activate
gigbot % make all
```

## Deploy

```zsh
gigbot % make deploy ENV=test
```

This will build three docker images and try to start the containers.  They will probably all fail.  That's OK:
* gigbot
* redis
* [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api)

## Signal

This is probably the most difficult bit.  The tl/dr is that you need to do one of two things:

* Set up your new dockerised `signal-cli-rest-api` as the primary Signal device on a Signal account
* Set it up as a linked device to an existing account

### Configure as Primary Device

If you have a Signal account on your phone and you love and cherish those sweet messages then you should probably *not* try to transfer that account to `signal-cli-rest-api` as primary.  Signal's phone clients are cold and brutal about information security and they would rather you lose everything than risk leakage.  There are ways round this for Android while the iPhone has no support for message migration outside the phone world.  I've never done either; don't ask me.

#### Preparation

* Make some `bash` scripts to guide the process
* Have some way to receive either an SMS or a call on the number you are registering
* Read through the execution steps so you know what's coming
* Read through the execution steps again so you know which ones are time critical

#### Execution

Execute the following steps in order.  Don't try to optimise: just execute.

* Make some `bash` scripts

1. `signal_registration_1_sms.sh`

```bash
    # See the signal-cli docs for voice registration.  I've never tried it.
    curl -X POST -H "Content-Type: application/json" \
        'http://signal:8010/v1/register/<International phone number>'
    # If this works then go to script 3
    # It will probably fail so solve the captcha at the link you get.
    # There will be a button which you can right click to get the link
    # Edit the link to remove the protocol bit - `signalcaptcha://`
    # Paste the code into script 2.
    # 
    # You have 30s to do all this after you solve the capture
```

2. `signal_registration_2_captcha.sh`

```bash
    # Paste the captcha into the -d json string below... remove the protcol before running
    curl -X POST -H "Content-Type: application/json" \
        -d '{"captcha":"PASTE HERE"}' \
        'http://signal:8010/v1/register/<International phone number>'
```

3. `signal_registration_3_verify.sh`

```bash
    # Note the two fields below... hopefully you got a text...
    curl -X POST -H "Content-Type: application/json" \
        'http://localhost:8010/v1/register/<International phone number>/verify/<SMS code>'
```

4. `signal_registration_4_profile.sh`

```bash
    # what do you want this Signal account to be called?.. gigbot?
    curl -X PUT -H "Content-Type: application/json" \
        -d '{"name": "<Signal name>"}' \
        'http://signal:8010/v1/profiles/<gigbot's nternational phone number>'
```

5. `signal_registration_5_send.sh`

```bash
    # Note the two numbers to fill in below
    curl -X POST -H "Content-Type: application/json" -d \
        '{"message": "gigbot messaging individuals", \
        "number": "<gigbot's international phone number>",
        "recipients": ["+<International phone number>"]}' \
        'http://signal:8010/v2/send'
```

6. `signal_registration_6_receive.sh`

```bash
    # You're getting the hang of this now... but you probably don't need this script
    # It's only required if you switched json-rpc off in the docker-compose.yml
    # ... why would you do that?  Still, no harm if you run this anyway
    curl -X GET -H "Content-Type: application/json" \
        'http://localhost:8010/v1/receive/<International phone number>'
```

7. `signal_registration_7_groups.sh`

```bash
    # Finally something useful.
    # This gives you the ID's of all the groups your bot is in... which might be none
    # So... add gigbot to some groups and do this again...
    # Pick the one you want to log to and add it to config/test.env
    curl -X GET -H "Content-Type: application/json" \
        'http://localhost:8010/v1/groups/<International phone number>'
```


### Configure as Linked Device

Not tried yet...
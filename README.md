# Forwarding bot

[![Downloads](https://pepy.tech/badge/forwarding-bot)](https://pepy.tech/project/forwarding-bot)
[![Downloads](https://pepy.tech/badge/forwarding-bot/month)](https://pepy.tech/project/forwarding-bot/month)
[![Downloads](https://pepy.tech/badge/forwarding-bot/week)](https://pepy.tech/project/forwarding-bot/week)

[![Code checks](https://github.com/dhvcc/forwarding-bot/workflows/Code%20checks/badge.svg)](https://github.com/dhvcc/forwarding-bot/actions?query=workflow%3A%22Code+checks%22)
[![Pypi publish](https://github.com/dhvcc/forwarding-bot/workflows/Publish%20Package%20to%20PyPI/badge.svg)](https://github.com/dhvcc/forwarding-bot/actions?query=workflow%3A%22Publish+Package+to+PyPI%22)

### Not really scalable, but straightforward one-way VK->TG message forwarding bot

Forward your VK conversation messages to TG

# Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

`pre-commit` usage is highly recommended

install hooks via `pre-commit install -t=pre-commit -t=pre-push`

# License

[MIT](https://github.com/dhvcc/forwarding-bot/blob/master/LICENSE)

# Documentation

1. [Installation](https://github.com/dhvcc/forwarding-bot#installation)
    1. [From PyPi](https://github.com/dhvcc/forwarding-bot#from-pypi)
    2. [From GitHub](https://github.com/dhvcc/forwarding-bot#from-github)
    3. [Extras](https://github.com/dhvcc/forwarding-bot#extras)
2. [Config](https://github.com/dhvcc/forwarding-bot#config)
    1. [Config source priority](https://github.com/dhvcc/forwarding-bot#config-argument-sources-are-prioritized)
    2. [Command-line arguments](https://github.com/dhvcc/forwarding-bot#command-line-arguments)
    3. [INI configs](https://github.com/dhvcc/forwarding-bot#ini-configs)
    4. [Environment variables](https://github.com/dhvcc/forwarding-bot#environment-variables)
        1. [Using environment variables](https://github.com/dhvcc/forwarding-bot#using-environment-variables)

# Installation

### From PyPi

```bash
pip install forwarding-bot
```

### From GitHub

```bash
git clone https://github.com/dhvcc/forwarding-bot.git
cd forwarding-bot
pip install .
```

### Extras

You can install extra dependencies, such as `speedups` or `dev`

```bash
pip install forwarding-bot[dev]
```
```bash
# You must be in a directory where setup.py is located
pip install .[speedups]
```
```bash
pip install forwarding-bot[speedups,dev]
```

# Config

## Config argument sources are prioritized

 1. Command-line arguments
 2. Local `.forwarding-bot` config
 3. Environment variables
 4. Global `{HOME}/.forwarding-bot` config


## Command-line arguments

To view help on cli arguments you can run `forwarding-bot --help`

## INI configs

Every argument is optional if config and will be grabbed from other source if not present
The syntax for config is the following:

```ini
[forwarding-bot]
BOT_TOKEN =
GROUP_TOKEN =
SOURCE_ID =
DESTINATION_ID =
```

**Local/global INI configs must be named `.forwarding-bot`**

**Global config must be located in your home folder**

## Environment variables

Env vars should be prefixed with `FORWARDING_BOT_`, for example, `FORWARDING_BOT_BOT_TOKEN`

### Using environment variables

[Windows](http://www.dowdandassociates.com/blog/content/howto-set-an-environment-variable-in-windows-command-line-and-registry/)

[Linux](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)

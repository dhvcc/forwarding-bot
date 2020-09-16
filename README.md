# Not really scalable, but straightforward one-way VK->TG message forwarding bot

Forward VK conversation messages to TG

## Installation and usage

### GitHub

1. Clone the repo `git clone https://github.com/dhvcc/forwarding-bot.git`

2. Initialize virtual environment `./init/venv.sh` or `virtualenv venv` `source venv/bin/activate` `pip install -r requirements.txt`

3. Set `config.json` variables (copy `config_sample.json`)

4. Run the module `source venv/bin/activate` `python -m forwarding_bot`

### Pip

1. Install via `pip install forwarding-bot`

2. Run the module `forwarding-bot`

## Windows

The readme is aimed at the Linux user, but you should be able to make it run on Windows

`uvloop` is currently not supported on Windows

## Contributing

`pre-commit` usage is highly recommended

install hooks via `pre-commit install -t=pre-commit -t=pre-push`
# Not really scalable, but straightforward VK to TG message transfer bot

Transfer VK conversation messages to TG

## Installation and usage

1. Clone the repo `git clone https://github.com/dhvcc/VK-TG-transfer-bot.git`

2. Initialize virtual environment `./init/venv.sh` or `virtualenv venv` `source venv/bin/activate` `pip install -r requirements.txt`

3. Set `transfer_bot/config` variables (not using env and services for simplicity)

4. Run the module `source venv/bin/activate` `python -m transfer_bot`

## Windows

The readme is aimed at the Linux user, but you should be able to make it run on Windows

## Contributing

`pre-commit` usage is highly recommended

install hooks via `pre-commit install -t=pre-commit -t=pre-push`
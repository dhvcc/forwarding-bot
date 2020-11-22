# Forwarding bot

### Перенесите свою беседу в Telegram

[![Downloads](https://pepy.tech/badge/forwarding-bot)](https://pepy.tech/project/forwarding-bot)
[![Downloads](https://pepy.tech/badge/forwarding-bot/month)](https://pepy.tech/project/forwarding-bot/month)
[![Downloads](https://pepy.tech/badge/forwarding-bot/week)](https://pepy.tech/project/forwarding-bot/week)

[![PyPI version](https://img.shields.io/pypi/v/forwarding-bot)](https://pypi.org/project/forwarding-bot)
[![Python versions](https://img.shields.io/pypi/pyversions/forwarding-bot)](https://pypi.org/project/forwarding-bot)
[![Wheel status](https://img.shields.io/pypi/wheel/forwarding-bot)](https://pypi.org/project/forwarding-bot)
[![License](https://img.shields.io/pypi/l/forwarding-bot?color=success)](https://github.com/dhvcc/forwarding-bot/blob/master/LICENSE)

[![Code checks](https://github.com/dhvcc/forwarding-bot/workflows/Code%20checks/badge.svg)](https://github.com/dhvcc/forwarding-bot/actions?query=workflow%3A%22Code+checks%22)
[![Pypi publish](https://github.com/dhvcc/forwarding-bot/workflows/Publish%20Package%20to%20PyPI/badge.svg)](https://github.com/dhvcc/forwarding-bot/actions?query=workflow%3A%22Publish+Package+to+PyPI%22)


# Суть проблемы

У вас есть некая беседа в VK, которую вы хотели бы перенести в Telegram, однако в ту беседу до сих пор приходят важные оповещения, туда пересылают документы

**Да, плохо, но не всё потеряно**

Ведь можно запустить бота, который будет каждое сообщение из беседы VK в ваш чат в Telegram

# Почему Telegram?

## Как пользователь

1. **Безопасность**. Вконтакте не особо задумываетсяо вашей безопасности и все **даже удалённые** сообщения хранятся у них. В любой момент этим могут воспользоваться заинтересованные личности
2. **Скорость** . Вконтакте работает медленно, сообщения долго грузятся
3. **Приоритеты**. К сожалени, главеный приоритет Вконтакте сейчас - деньги, а не  юзабельность/скорость/безопасность. Вот так мы и получаем бесполезные VK Clips, VK Connect и модный VK Messenger
4. Да и вообще, у них стикеры платные

## Как разработчик

1. **Баги, баги**, много багов. Только вот вместе иправления ты слышишь "мы добавили в бэклог, скоро исправим". Нет, не исправляете
2. **Плохая документация API**, которая не всегда отражает истину
3. Ссылки на пункты статьи не имеют аттрибутов `id`, то есть нельзя сделать `vk.com/dev/метод?#пункт`. VK API имеет свой необычный и совершенно неудобный механизм ссылок на пункты

## Как работает бот?

Бот находится в беседе VK и в чате Telegram

Бот слушает беседу и ждёт новое сообщение. Как только оно приходит бот приводит сообщение в подобающий вид и отправляет его в другую беседу в Telegram

## Примеры работы

**VK**

![VK](https://i.imgur.com/f4yiWBv.png)

**Telegram**

`документ_0` и `документ_1` это ссылки на сообщения, которые содержат документ

![TG](https://i.imgur.com/X1LGL3w.png)

## Быстрый старт

### Что нужно?

1. Ключ доступа одного из администраторов группы. Получить его можно авторизовавшись через приложение VK. Удобно это сделать можно [тут](https://vkhost.github.io/)
    - Почему не токен группы? К сожалению, в ВК есть баг, из-за которого могут теряться вложения, поэтому нужно перезапрашивать данные о сообщении
    - Бот группы не имеет доступа к истории сообщений, а юзер имеет. Почему? Я не знаю
    - Они собираются это изменить, но навряд ли это скоро произойдёт
    - Код программы открытый, так что токены чужие никто воровать не собирается
2. Бот в Telegram, который будет находиться в другой беседе и слать туда сообщения. Создать бота можно написав пользователю [@BotFather](https://t.me/botfather)
3. ID беседы VK. Для пользователь, от лица которого будет работать бот должен зайти в беседу и извлечь ID из адресной строки. Например, в адресе `https://vk.com/im?sel=c123456`, `123456` - это и есть ID беседы
4. ID чата Telegram. Получить его способов много, однако я предпочитаю просто пригласить в беседу [@getidsbot](https://t.me/getidsbot)

### Установка

### PyPi

```bash
pip install forwarding-bot
```

### GitHub

```bash
git clone https://github.com/dhvcc/forwarding-bot.git
cd forwarding-bot
pip install .
```

### Дополнительно

Вы можете установить дополнительные зависимости

`speedups` ускорят работу бота, а `dev` установит необходимые зависимости для разработки

```bash
pip install forwarding-bot[dev]
```
```bash
# Вы должны находится в папке, где расположен setup.py (если скачивали с GitHub)
pip install .[speedups]
```
```bash
pip install forwarding-bot[speedups,dev]
```
### Настройка

В папке, откуда будете запускать бота создайте файл `.forwarding-bot` и запишите в него следующее

```ini
[forwarding-bot]
BOT_TOKEN =
USER_TOKEN =
SOURCE_ID =
DESTINATION_ID =
```

Далее заполните файл данными. Про получение данных обратитесь к пункту [Что нужно?](https://github.com/dhvcc/forwarding-bot#что-нужно)

- В `BOT_TOKEN` запишите ключ доступа Telegram бота, который вы получили от BotFather
- В `USER_TOKEN` запишите ключ доступа одного из администраторов беседы VK
- В `SOURCE_ID` запишите ID беседы VK
- В `DESTINATION_ID` запишите ID чата Telegram


### Запуск

После настройки, зайдите в папку, где лежит ваш `.forwarding-bot` и запустите `python -m forwarding-bot` (что бы запустить в фоновом режиме добавьте в конце команды `&`)

# Дополнительно

...

# Помочь развитию

Пулл реквесты приветствуются. Что бы внести большие изменения, пожалуйста, откройте сначала `issue`, что бы обсудить изменения

Рекоммендуется использование `pre-commit`. Установить git хуки `pre-commit install -t=pre-commit -t=pre-push`

# Лицензия

[MIT](https://github.com/dhvcc/forwarding-bot/blob/master/LICENSE)
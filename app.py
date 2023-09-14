import json

import telebot

from extensions import APIConnector, APIException, parse_supported_codes
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def str_supported_codes() -> str:
    supported_codes_list = parse_supported_codes()
    text = "Доступные коды валют: "
    for i in supported_codes_list:
        str_codes = " - ".join(i)
        text = "\n".join(
            (
                text,
                str_codes,
            )
        )
    return text


@bot.message_handler(commands=["start", "help"])
def bot_help(message: telebot.types.Message) -> None:
    text = "Введите через пробел: \
<код конвертируемой валюты> <код валюты, в которую нужна конвертация> <количество конвертируемой валюты>\
\nПример корректного запроса: EUR USD 10\
\nПри помощи /values можно получить список доступных кодов валют"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def bot_values(message: telebot.types.Message) -> None:
    text = str_supported_codes()
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message) -> None:
    try:
        user_values = message.text.split(" ")

        if len(user_values) != 3:
            raise APIException(
                f"Ожидается 3 параметра, разделенных пробелом, получено: {len(user_values)}"
            )

        base, quote, amount = user_values

        parse_req = json.loads(APIConnector.get_price(base.upper(), quote.upper(), amount))
        price = parse_req["conversion_result"]
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду, ошибка бота: {e}')
    else:
        text = f"Цена {amount} {base.upper()} в {quote.upper()} составит - {price}"
        bot.reply_to(message, text)


bot.polling()

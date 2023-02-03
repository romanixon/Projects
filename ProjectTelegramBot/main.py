import telebot
from config import keys, TOKEN
from extensions import APIExeption, ValueConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Введи валюту в формате:\n (имя валюты) \
(имя валюты в которую перевести) \
(количество переводимой валюты), \
 выбрать валюты: /values         '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values_ = message.text.split(' ')
        values_ = list(map(str.lower, values_))
        if len(values_) != 3:
            raise APIExeption('Слишком много параметров')

        quote, base, amount = values_
        final_base = ValueConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {final_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
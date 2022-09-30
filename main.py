from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json
from SimpleQIWI import *
from time import sleep

with open('config.json') as f:
   config = json.load(f)

TOKEN = config['token']
phone = config['qiwinumber']
token = config['qiwitoken']
api = QApi(token=token, phone=phone)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

base = []
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    button_hi = KeyboardButton('🎓 Хочу получить ответы!')

    hi = ReplyKeyboardMarkup(resize_keyboard=True)
    hi.add(button_hi)
            
    await bot.send_photo(message.chat.id, photo='https://media.discordapp.net/attachments/1018941949778071594/1025400185934860288/by_devor.png?width=696&height=663', 
                        caption=f"🖐 Привет, {message.from_user.first_name}\n\nЭтот бот может найти ОТВЕТЫ ОГЭ ЕГЭ И МНОГИЕ ДРУГИЕ📔\n\n👇 Нажми на кнопку ниже и получи ответы меньше за минуту.", reply_markup=hi)


@dp.message_handler(Text(equals='🎓 Хочу получить ответы!'))
async def klass(message: types.Message):

    value = config['value']
    inline_btn_1 = InlineKeyboardButton('💸 ОПЛАТИТЬ', callback_data='button1')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    if isinstance(value, int) == True:
        await message.reply(f'Для начала работы нужно оплатить подписку за {value}₽\nКакие конкретные работы будут?\n— ВПР (Всероссийские Проверочные Работы)\n— СтатГрад (все материалы системы)\n— КДР и МЦКО (все классы)\n— РДР и НИКО (все классы)\n— ДКР и РПР (все классы)\n— ВОШ (Всероссийская Олимпиада Школьников) - школьный этап\n— Конкурсы: Русский Медвежонок, Кенгуру, КИТ, Золоте Руно, Британский Бульдог, ЧИП и другие.\n', reply_markup=inline_kb1)
    else:
        print('Error: Введите правильное число в config.json')


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    qiwinick = config['qiwinick']
    inline_btn_1 = InlineKeyboardButton('⏰ ССЫЛКА', url=f'https://qiwi.com/n/{qiwinick}', callback_data='button2')
    inline_btn_2 = InlineKeyboardButton('💸 ОПЛАТИЛ', callback_data='button3')
    inline_kb2 = InlineKeyboardMarkup().add(inline_btn_2, inline_btn_1)
    price = config['value']                   
    comment = api.bill(price)                               

    await bot.send_message(callback_query.from_user.id, f'ОПЛАТА: QIWI,\nКомментарий - {comment}\nНик киви - {qiwinick}\nСумма - {price}',reply_markup=inline_kb2)

    base.append(comment)

@dp.callback_query_handler(lambda c: c.data == 'button3')
async def oplata(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    api.start()                 
    if base != []:
        for i in base:
            if api.check(i):
                print("Платёж получен!")
                await bot.send_message(config['owner_id'], f'💸 Поступила новая оплата.\nID: {callback_query.from_user.id}\nNICK: {callback_query.from_user.first_name}')
                base.remove(i)
                break
        
        api.stop()

        await bot.send_message(callback_query.from_user.id,'Платеж не поступил, попробуйте снова через несколько минут')
    else:
        await bot.send_message(callback_query.from_user.id,'Платеж не поступил, попробуйте снова через несколько минут')

if __name__ == '__main__':
    executor.start_polling(dp)
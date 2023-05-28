TOKEN = "6262650098:AAFPFegRI2ZSsR1RUXBwJZEBFuUTG9bvJDE"
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
import random
proxy_url = 'http://proxy.server:3128'
bot = Bot(token=TOKEN, proxy=proxy_url)
dp = Dispatcher(bot, storage=MemoryStorage())
data = open('data.txt','r')
lns=data.readlines()
users_coins =eval(lns[0])
users_inv=eval(lns[1])
users_cats=eval(lns[2])
admins = [1900123193]
data.close()
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('/meow')
button2 = types.KeyboardButton('/leaderboard')
button3 = types.KeyboardButton('/buy_cat')
button4 = types.KeyboardButton('/help')
button5 = types.KeyboardButton('/inventory')
keyboard.add(button1, button2, button3, button4, button5)
def render_keyboard(user_id,users_inv):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('/eat кототорт')
    button2 = types.KeyboardButton('/eat котерброд')
    button3 = types.KeyboardButton('/eat соленая рыбка')
    button4 = types.KeyboardButton('/menu')
    keyboard.add(button1, button2, button3, button4)
    return keyboard
@dp.message_handler(Command('start'))
async def start(message: types.Message):
    response = "Приветствую тебя, уважаемый пользователь! Я бот игры про мяукующих котиков.\n"
    response += "С моей помощью ты сможешь мяукать, зарабатывать мяукоины и участвовать в захватывающих соревнованиях.\n"
    response += "Давай начнем наше приключение вместе!\n"
    response += "Используй команду /help, чтобы узнать больше.\n"
    response += "Приготовься к приключениям и не забудь погладить своего виртуального котика! Удачи!"
    await message.reply(response, reply_markup=keyboard)
@dp.message_handler(Command('meow'))
async def meow(message: types.Message):
    user_id = message.chat.id
    if user_id not in users_coins:
        users_coins[user_id] = 0
    if user_id not in users_cats:
        users_cats[user_id] = 1
    if user_id not in users_inv:
        users_inv[user_id]=[0,0,0]
    r=random.randint(0,10000)
    if r==1:
        users_inv[user_id][2]+=1
        await message.reply("Мяу! Вы получили легендарный предмет:кототорт(х10).", reply_markup=keyboard)
    elif r in list(range(2,102)):
        users_inv[user_id][1]+=1
        await message.reply("Мяу! Вы получили эпический предмет:котерброд(х5).", reply_markup=keyboard)
    elif r in list(range(103,1103)):
        users_inv[user_id][0]+=1
        await message.reply("Мяу! Вы получили редкий предмет:соленая рыбка(х2).", reply_markup=keyboard)
    else:
        s=abs(users_cats[user_id]*random.randint(-50,50)+random.randint(0,9))//11
        users_coins[user_id] += s
        await message.reply("Мяу! Вы получили мяукоинов:"+str(s)+".", reply_markup=keyboard)
@dp.message_handler(Command('leaderboard'))
async def leaderboard(message: types.Message):
    response = "Турнирная таблица:\n"
    sorted_users = sorted(users_coins.items(), key=lambda x: x[1], reverse=True)
    for i, (user_id, coins) in enumerate(sorted_users, start=1):
        username = await bot.get_chat(user_id)
        response += f"{i}. @{username.username} - {coins} мяукоинов\n"
    await message.reply(response, reply_markup=keyboard)
@dp.message_handler(Command('buy_cat'))
async def buy_cat(message: types.Message):
    user_id = message.chat.id
    if user_id not in users_coins:
        users_coins[user_id] = 0
    coins = users_coins[user_id]
    if coins >= int(10*(users_cats[user_id]*2**0.5))-4 and coins>0:
        users_coins[user_id] -= int(10*(users_cats[user_id]*2**0.5))-4
        await message.reply("Поздравляем! Вы купили котика за "+str(int(10*(users_cats[user_id]*2**0.5))-4)+" мяукоинов. Мяу!", reply_markup=keyboard)
        users_cats[user_id]+=1
    else:
        await message.reply("У вас недостаточно мяукоинов для покупки котика, нужно:"+str(int(10*(users_cats[user_id]*2**0.5))-4), reply_markup=keyboard)
@dp.message_handler(Command('inventory'))
async def invent(message: types.Message):
    user_id=message.from_user.id
    await message.reply("Эта функция в разработке",reply_markup=render_keyboard(user_id, users_inv))
@dp.message_handler(Command('help'))
async def help_command(message: types.Message):
    response = "Я рад, что ты обратился за помощью! Вот список доступных команд и их описание:\n"
    response += "/meow - Мяукни и получи мяукоин.\n"
    response += "/leaderboard - Показать турнирную таблицу и узнать, насколько ты приблизился к вершине.\n"
    response += "/buy_cat - Купить котика за 10 мяукоинов и расширить свою кошачью армию.\n"
    response += "/help - Отобразить список команд и их описание.\n"
    response += "Приготовься к приключениям и не забудь погладить своего виртуального котика! Удачи!"
    await message.reply(response, reply_markup=keyboard)
@dp.message_handler(Command('add_coins'))
async def add_coins(message: types.Message):
    if message.from_user.id in admins:
        txt=message.text.split(" ")
        if len(txt)>1:
            coins=int(txt[1])
            if len(txt)>2:
                user_id=int(txt[2])
            else:
                user_id=message.chat.id
        else:
            coins=100
            user_id=message.chat.id
        if user_id not in users_coins:
            users_coins[user_id] = 0
        users_coins[user_id] += coins
        await message.reply(f"Пользователю {user_id} добавлено {coins} мяукоинов.", reply_markup=keyboard)
@dp.message_handler(Command('add_cats'))
async def add_cats(message: types.Message):
    if message.from_user.id in admins:
        txt=message.text.split(" ")
        if len(txt)>1:
            cats=int(txt[1])
            if len(txt)>2:
                user_id=int(txt[2])
            else:
                user_id=message.chat.id
        else:
            cats=10
            user_id=message.chat.id
        if user_id not in users_cats:
            users_cats[user_id] = 0
        users_cats[user_id] += cats
        await message.reply(f"Пользователю {user_id} добавлено {cats} котиков.", reply_markup=keyboard)

if __name__ == '__main__':
    from aiogram.utils import executor
    executor.start_polling(dp, skip_updates=True)
print(users_coins)
print(users_cats)
data = open('data.txt','w')
data.write(repr(users_coins)+'\n')
data.write(repr(users_inv)+'\n')
data.write(repr(users_cats)+'\n')
data.close
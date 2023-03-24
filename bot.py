"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types

from decouple import config

from random import randint

API_TOKEN = config('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


expected_result = 0
expressions = 0
points = 0
correct = 0
incorrect = 0

def get_expression():
    global expected_result
    actions = ["+", "-", "/", "*"]
    expression = f'{randint(1, 10)} {actions[randint(0, len(actions) - 1)]} {randint(1, 10)}'
    expected_result = eval(expression)
    return expression

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message,):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    global expressions
    await message.reply(f"Hi!\nI'm CalcBot!\nPowered by aiogram.\nHere is the first expression:\n{get_expression()}")

@dp.message_handler(commands='stop_game')
async def end_game(message: types.Message):
    global expressions, points, correct, incorrect
    await message.reply(f'Your points are {points}.\nYou have solved {expressions} expressions with {correct} correct and {incorrect} incorrect')
    if correct > incorrect:
        await message.answer_sticker('CAACAgIAAxkBAAO4ZB1-A9MX59vmibaK5X9KfQABopfdAAIlAAM7YCQUglfAqB1EIS0vBA')
    else:
        await message.answer_sticker('CAACAgIAAxkBAAO6ZB1-FUbdundpdB1D_d2V-pRgL6gAAjYAAztgJBTr3UJw-qIU0S8E')
    expressions = 0
    points = 0
    correct = 0
    incorrect = 0

@dp.message_handler()
async def echo(message: types.Message):
    global expressions, points, correct, incorrect
    expressions = expressions + 1
    reply = ''
    if float(message.text) == float(expected_result):
        correct = correct + 1
        points = points + 1
        reply = 'points +1\n'
    else:
        incorrect = incorrect + 1
        if points > 0:
            points = points - 1
            reply = 'points -1\n'
    await message.answer(f'{reply}{get_expression()}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
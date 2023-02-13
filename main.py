import json
import os
import uuid
from dotenv import load_dotenv
from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
import redis
import hashlib
import random
import requests
import jmespath
from datetime import datetime as dt
from aiogram import types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
import constants

load_dotenv("var.env")
TOKEN = os.getenv('TELEGRAM_TOKEN')
r = redis.Redis(host=os.getenv('REDIS_HOST'),
                password=os.getenv('REDIS_PASSWORD'),
                decode_responses=True, db=0)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
ex_temp_array = 6000
ex_event = 20000

abb_array = ["MTL",
None,
None,
None,
"TOR",
"BOS",
None,
None,
None,
"NYR",
"CHI",
"DET",
None,
"LAK",
"DAL",
"PHI",
"PIT",
"STL",
"BUF",
"VAN",
"CGY",
"NYI",
"NJD",
"WSH",
"EDM",
"CAR",
"COL",
"ARI",
"SJS",
"OTT",
"TBL",
"ANA",
"FLA",
"NSH",
"WPG",
"CBJ",
"MIN",
"VGK",
"SEA"]

teams = [{"team_id": 1, "fr_id": 23, "abb": "NJD"}, {"team_id": 2, "fr_id": 22, "abb": "NYI"},
         {"team_id": 3, "fr_id": 10, "abb": "NYR"}, {"team_id": 4, "fr_id": 16, "abb": "PHI"},
         {"team_id": 5, "fr_id": 17, "abb": "PIT"}, {"team_id": 6, "fr_id": 6, "abb": "BOS"},
         {"team_id": 7, "fr_id": 19, "abb": "BUF"}, {"team_id": 8, "fr_id": 1, "abb": "MTL"},
         {"team_id": 9, "fr_id": 30, "abb": "OTT"}, {"team_id": 10, "fr_id": 5, "abb": "TOR"},
         {"team_id": 12, "fr_id": 26, "abb": "CAR"}, {"team_id": 13, "fr_id": 33, "abb": "FLA"},
         {"team_id": 14, "fr_id": 31, "abb": "TBL"}, {"team_id": 15, "fr_id": 24, "abb": "WSH"},
         {"team_id": 16, "fr_id": 11, "abb": "CHI"}, {"team_id": 17, "fr_id": 12, "abb": "DET"},
         {"team_id": 18, "fr_id": 34, "abb": "NSH"}, {"team_id": 19, "fr_id": 18, "abb": "STL"},
         {"team_id": 20, "fr_id": 21, "abb": "CGY"}, {"team_id": 21, "fr_id": 27, "abb": "COL"},
         {"team_id": 22, "fr_id": 25, "abb": "EDM"}, {"team_id": 23, "fr_id": 20, "abb": "VAN"},
         {"team_id": 24, "fr_id": 32, "abb": "ANA"}, {"team_id": 25, "fr_id": 15, "abb": "DAL"},
         {"team_id": 26, "fr_id": 14, "abb": "LAK"}, {"team_id": 28, "fr_id": 29, "abb": "SJS"},
         {"team_id": 29, "fr_id": 36, "abb": "CBJ"}, {"team_id": 30, "fr_id": 37, "abb": "MIN"},
         {"team_id": 52, "fr_id": 35, "abb": "WPG"}, {"team_id": 53, "fr_id": 28, "abb": "ARI"},
         {"team_id": 54, "fr_id": 38, "abb": "VGK"}, {"team_id": 55, "fr_id": 39, "abb": "SEA"}]


def get_last_games(id, fr_id):
    url = 'https://statsapi.web.nhl.com/api/v1/schedule?site=en_nhl&startDate=2023-02-01&endDate=2023-02-28&teamId=' + str(id)
    querystring = {}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring, timeout=3)
    games = jmespath.search(
        "dates[].games[].{homeid: teams.home.team.id, awayid: teams.away.team.id, gamestate: status.detailedState, date: gameDate, home: teams.home.team.name, homescore: teams.home.score, awayscore: teams.away.score, away: teams.away.team.name}",
        json.loads(response.text))
    final_games = ""
    for game in games:
        if game['gamestate'] == "Final":
            final_games = final_games + abb(game['homeid']) + " " + str(game['homescore']) + "-" + str(
                game['awayscore']) + " " + abb(game['awayid']) + "\n"
    print(final_games)
    return final_games


def abb(id):
    return abb_array[int(id) - 1]


def api_request(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
    except requests.exceptions.Timeout as e:
        # Обработка ошибки тайм-аута
        print("Timeout error:", e)
        res = "HTTPS ERROR"
        return res
    except requests.exceptions.HTTPError as e:
        # Обработка ошибок HTTP
        print("HTTP error:", e)
    except requests.exceptions.RequestException as e:
        # Обработка всех остальных исключений
        print("Request exception:", e)
    else:
        # Обработка успешного запроса
        print("Successful response:", response.text)
        return response.text


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        # types.BotCommand("start", "Start"),
        types.BotCommand("teams", "Команды")
    ])


@dp.message_handler(commands=['debug'])
async def handler_debug(message: types.Message):
    get_last_games(6)


@dp.message_handler(commands=['teams'])
async def handler_teams(message: types.Message):
    await message.delete()
    teams_kb = []
    for team in teams:
        fr_id = str(team['fr_id'])
        team_id = str(team['team_id'])
        teams_kb.append(types.InlineKeyboardButton(text=team['abb'],
                                                   callback_data="TEAM:" + team_id + ":" + fr_id))
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(*teams_kb)
    await message.answer("Выберите из списка", reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data.startswith("TEAM"))
async def handler_team(call: types.CallbackQuery):
    await call.message.edit_text("<code>Загрузка...</code>")
    team_id = call.data.split(":")[1]
    fr_id = call.data.split(":")[2]
    print(call.data)
    print(abb(fr_id))
    url = 'https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"},{"property":"playerId","direction":"ASC"}]&start=0&limit=5&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId=' + str(
        fr_id) + ' and gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023'
    response = api_request(url)
    leaders_list = ""
    if response.startswith("HTTPS"):
        await call.message.edit_text("Ошибка соединения с сервером. Попробуйте еще раз.")
    else:
        for leader in json.loads(response)['data']:
            leaders_list = leaders_list + leader['lastName'] + " [" + str(leader['goals']) + "-" + str(
                leader['assists']) + "-" + str(leader['points']) + "]\n"
        await call.message.edit_text(
            "Лидеры <b>" + call.data.split(":")[2] + "</b>\n" + leaders_list + "\nПоследние игры:\n")
        print(get_last_games(team_id, fr_id))


if __name__ == '__main__':
    # print(redis.client_info())
    print('Started ' + str(dt.now()), flush=True)
    # executor.start_polling(dp, skip_updates=True)
    executor.start_polling(dp, on_startup=set_default_commands)

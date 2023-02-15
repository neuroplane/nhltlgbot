import requests
import jmespath
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import aiogram.utils.markdown as fmt
from aiogram.utils import executor
import datetime as dt
import random


TOKEN = '6029510223:AAGRPrBqvX47ggV6XsU2BtQIVZ0rqMZtu6I'

teams = [{"team_name": "New Jersey Devils", "team_id": 1, "fr_id": 23, "abb": "NJD"},
         {"team_name": "New York Islanders", "team_id": 2, "fr_id": 22, "abb": "NYI"},
         {"team_name": "New York Rangers", "team_id": 3, "fr_id": 10, "abb": "NYR"},
         {"team_name": "Philadelphia Flyers", "team_id": 4, "fr_id": 16, "abb": "PHI"},
         {"team_name": "Pittsburgh Penguins", "team_id": 5, "fr_id": 17, "abb": "PIT"},
         {"team_name": "Boston Bruins", "team_id": 6, "fr_id": 6, "abb": "BOS"},
         {"team_name": "Buffalo Sabres", "team_id": 7, "fr_id": 19, "abb": "BUF"},
         {"team_name": "Montréal Canadiens", "team_id": 8, "fr_id": 1, "abb": "MTL"},
         {"team_name": "Ottawa Senators", "team_id": 9, "fr_id": 30, "abb": "OTT"},
         {"team_name": "Toronto Maple Leafs", "team_id": 10, "fr_id": 5, "abb": "TOR"},
         {"team_name": "Carolina Hurricanes", "team_id": 12, "fr_id": 26, "abb": "CAR"},
         {"team_name": "Florida Panthers", "team_id": 13, "fr_id": 33, "abb": "FLA"},
         {"team_name": "Tampa Bay Lightning", "team_id": 14, "fr_id": 31, "abb": "TBL"},
         {"team_name": "Washington Capitals", "team_id": 15, "fr_id": 24, "abb": "WSH"},
         {"team_name": "Chicago Blackhawks", "team_id": 16, "fr_id": 11, "abb": "CHI"},
         {"team_name": "Detroit Red Wings", "team_id": 17, "fr_id": 12, "abb": "DET"},
         {"team_name": "Nashville Predators", "team_id": 18, "fr_id": 34, "abb": "NSH"},
         {"team_name": "St. Louis Blues", "team_id": 19, "fr_id": 18, "abb": "STL"},
         {"team_name": "Calgary Flames", "team_id": 20, "fr_id": 21, "abb": "CGY"},
         {"team_name": "Colorado Avalanche", "team_id": 21, "fr_id": 27, "abb": "COL"},
         {"team_name": "Edmonton Oilers", "team_id": 22, "fr_id": 25, "abb": "EDM"},
         {"team_name": "Vancouver Canucks", "team_id": 23, "fr_id": 20, "abb": "VAN"},
         {"team_name": "Anaheim Ducks", "team_id": 24, "fr_id": 32, "abb": "ANA"},
         {"team_name": "Dallas Stars", "team_id": 25, "fr_id": 15, "abb": "DAL"},
         {"team_name": "Los Angeles Kings", "team_id": 26, "fr_id": 14, "abb": "LAK"},
         {"team_name": "San Jose Sharks", "team_id": 28, "fr_id": 29, "abb": "SJS"},
         {"team_name": "Columbus Blue Jackets", "team_id": 29, "fr_id": 36, "abb": "CBJ"},
         {"team_name": "Minnesota Wild", "team_id": 30, "fr_id": 37, "abb": "MIN"},
         {"team_name": "Winnipeg Jets", "team_id": 52, "fr_id": 35, "abb": "WPG"},
         {"team_name": "Arizona Coyotes", "team_id": 53, "fr_id": 28, "abb": "ARI"},
         {"team_name": "Vegas Golden Knights", "team_id": 54, "fr_id": 38, "abb": "VGK"},
         {"team_name": "Seattle Kraken", "team_id": 55, "fr_id": 39, "abb": "SEA"}]


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def abbr(team_id):
    return next(filter(lambda a: a['team_id'] == team_id, teams))['abb']


def date_diff(days):
    return dt.datetime.fromisoformat(str(dt.datetime.date(dt.datetime.now() - dt.timedelta(days)))).strftime('%Y-%m-%d')


def get_last_games(team_id):
    url = 'https://statsapi.web.nhl.com/api/v1/schedule?site=en_nhl&startDate=' + date_diff(15) + '&endDate='+ dt.datetime.now().strftime('%Y-%m-%d') +'&teamId=' + str(
        team_id) + '&expand=schedule.teams,schedule.venue,schedule.metadata,schedule.game.seriesSummary,schedule.ticket,schedule.broadcasts.all,schedule.linescore,schedule.decisions,schedule.game.content.media.epg'
    print(url)
    querystring = {}
    payload = ""
    response = api_request(url)
    images = []
    games = jmespath.search(
        'dates[].games[].{image: content.media.epg[2].items[0].image.cuts."1136x640".src, link: content.media.epg[2].items[0].playbacks[4].url, awayabb: teams.away.team.abbreviation, homeabb: teams.home.team.abbreviation,homeid: teams.home.team.id, awayid: teams.away.team.id, gamestate: status.detailedState, date: gameDate, home: teams.home.team.name, homescore: teams.home.score, awayscore: teams.away.score, away: teams.away.team.name}',
        json.loads(response))
    final_games = ""
    for game in games:
        if game['image'] is not None:
            images.append(game['image'])
        if game['gamestate'] == "Final":
            final_games = final_games + "<code>" +game['homeabb'] + " " + str(game['homescore']) + "-" + str(
                game['awayscore']) + " " + game['awayabb'] + "</code> <a href='" + game['link']+"'>  🎦</a>\n"
    print(len(images), images)
    return final_games + "@" + images[random.randrange(0, len(images)-1)]


def api_request(url):
    try:
        response = requests.get(url, timeout=5)
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
        #print("Successful response:", response.text)
        return response.text


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        #types.BotCommand("start", "Start"),
        types.BotCommand("teams", "Информация по командам"),
        types.BotCommand("games", "Игры последнего дня"),
        types.BotCommand("standings", "Ситуация по конференциям")
    ])


@dp.message_handler(commands=['start'])
async def handler_debug(message: types.Message):
    await message.answer("Этот бот выдает лучших игроков и последние сыгранные матчи выбранной команды по запросу /teams.\n\nИногда серверы NHL отвечают долго. В этом случае просто отправьте запрос заново.")
    print(message.from_user.id)
    await bot.send_message(chat_id=5167284381, text="Начата работа с ботом")


@dp.message_handler(commands=['standings'])
async def handler_standings(message: types.Message):
    await message.delete()
    standings_str = ""
    standings = api_request('https://statsapi.web.nhl.com/api/v1/standings/byConference')
    standings_jmes = jmespath.search(
        'records[].{name: conference.name, standings: teamRecords[]. {name:team.name, wins: leagueRecord.wins, losses: leagueRecord.losses, ot: leagueRecord.ot, place: conferenceRank}}',
        json.loads(standings))
    print(standings_jmes)
    for conference in standings_jmes:
        print(conference['name'])
        standings_str = standings_str + "\n" + conference['name'] + "\n"
        for team in conference['standings']:
            print(team['place'], team['name'], team['wins'], team['losses'], team['ot'])
            standings_str = standings_str + str(team['place']) + ". <b>" + team['name'] + "</b> [" + str(team['wins']) + "-" + str(team['losses']) + "-" + str(team['ot']) + "]\n"
    await message.answer(standings_str)
    await bot.send_message(chat_id=5167284381, text="Запрос положения в конфе")


@dp.message_handler(commands=['teams'])
async def handler_teams(message: types.Message):
    await message.delete()
    teams_kb = []
    for team in teams:
        fr_id = str(team['fr_id'])
        team_id = str(team['team_id'])
        team_abb = str(team['abb'])
        team_name = str(team['team_name'])
        teams_kb.append(types.InlineKeyboardButton(text=team['abb'],
                                                   callback_data="TEAM:" + team_id + ":" + fr_id + ":" + team_abb + ":" + team_name))
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(*teams_kb)
    await message.answer("Выберите из списка", reply_markup=keyboard)
    print("+")
    await bot.send_message(chat_id=5167284381, text="Запрос команд")


@dp.callback_query_handler(lambda call: call.data.startswith("TEAM"))
async def handler_team(call: types.CallbackQuery):
    await call.message.edit_text("<code>Загрузка...</code>")
    team_id = call.data.split(":")[1]
    fr_id = call.data.split(":")[2]
    print(call.data)
    url = 'https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"},{"property":"playerId","direction":"ASC"}]&start=0&limit=5&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId=' + str(
        fr_id) + ' and gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023'
    response = api_request(url)
    leaders_list = ""
    if response.startswith("HTTPS"):
        # await call.message.edit_text("Сервер NHL отвечает слишком долго. Попробуйте еще раз.\n\n/teams")
        teams_kb = []
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        teams_kb.append(types.InlineKeyboardButton(text="Повторить запрос: " + call.data.split(":")[3],
                                                   callback_data=call.data.split(":")[0] + ":" + call.data.split(":")[1] + ":" + call.data.split(":")[2] + ":" + call.data.split(":")[3] + ":" + call.data.split(":")[4]))
        keyboard.add(*teams_kb)
        await call.message.edit_text(text="Сервер NHL отвечает слишком долго. Попробуйте еще раз.", reply_markup=keyboard)
    else:
        for leader in json.loads(response)['data']:
            leaders_list = leaders_list + leader['lastName'] + " " + str(leader['points']) + " (" + str(
                leader['goals']) + "+" + str(leader['assists']) + ")\n"
        last_games = get_last_games(team_id).split("@")
        final_message = "Лидеры <b>" + call.data.split(":")[
                4] + " [" + call.data.split(":")[
                3] + "]</b>\n\n" + leaders_list + "\nПоследние игры:\n\n" + last_games[0] + ""
        await call.message.delete()
        await call.message.answer_photo(photo=last_games[1], caption=final_message)
        '''await call.message.edit_text(
            "Лидеры <b>" + call.data.split(":")[
                4] + " [" + call.data.split(":")[
                3] + "]</b>\n\n" + leaders_list + "\nПоследние игры:\n\n" + get_last_games(team_id) + "" + fmt.hide_link('https://cms.nhl.bamgrid.com/images/photos/340820602/1704x960/cut.jpg'))'''
    await bot.send_message(chat_id=5167284381, text="Запрос " + call.data.split(":")[3])


@dp.message_handler(commands=['games'])
async def handler_games(message: types.Message):
    await message.delete()
    yesterday = date_diff(1)
    url = 'https://statsapi.web.nhl.com/api/v1/schedule?&date=' + yesterday + '&expand=schedule.game.content.media.epg'
    response = api_request(url)
    images = []
    latest_games_json = jmespath.search(
        'dates[].games[].{gamestate: status.detailedState, image: content.media.epg[2].items[0].image.cuts."1136x640".src, homeid: teams.home.team.id, awayid: teams.away.team.id, highlights: content.media.epg[2].items[0].playbacks[4].url, date: gameDate, status: status.statusCode, home: teams.home.team.name, away: teams.away.team.name, homescore: teams.home.score, awayscore: teams.away.score}',
        json.loads(response))
    final_games = ""
    for game in latest_games_json:
        if game['image'] is not None:
            images.append(game['image'])
        if game['gamestate'] == "Final":
            final_games = final_games + "<code>" + abbr(game['homeid']) + " " + str(game['homescore']) + "-" + str(
                game['awayscore']) + " " + abbr(game['awayid']) + "</code> <a href='" + game['highlights']+"'>  🎦</a>\n"
    await message.answer_photo(photo=images[random.randrange(0, len(images)-1)], caption="Игры за <code>" + date_diff(1) + "</code>\n\n" + final_games)
    await bot.send_message(chat_id=5167284381, text="Запрос игр")

if __name__ == '__main__':
    # print(redis.client_info())
    print('Started ' + str(dt.datetime.now()), flush=True)
    # executor.start_polling(dp, skip_updates=True)
    executor.start_polling(dp, on_startup=set_default_commands)

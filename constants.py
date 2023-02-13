team_list = [{"name": "Carolina Hurricanes", "abbreviation": "CAR", "id": 12},
             {"name": "New Jersey Devils", "abbreviation": "NJD", "id": 1},
             {"name": "New York Rangers", "abbreviation": "NYR", "id": 3},
             {"name": "Washington Capitals", "abbreviation": "WSH", "id": 15},
             {"name": "Pittsburgh Penguins", "abbreviation": "PIT", "id": 5},
             {"name": "New York Islanders", "abbreviation": "NYI", "id": 2},
             {"name": "Philadelphia Flyers", "abbreviation": "PHI", "id": 4},
             {"name": "Columbus Blue Jackets", "abbreviation": "CBJ", "id": 29},
             {"name": "Boston Bruins", "abbreviation": "BOS", "id": 6},
             {"name": "Toronto Maple Leafs", "abbreviation": "TOR", "id": 10},
             {"name": "Tampa Bay Lightning", "abbreviation": "TBL", "id": 14},
             {"name": "Florida Panthers", "abbreviation": "FLA", "id": 13},
             {"name": "Buffalo Sabres", "abbreviation": "BUF", "id": 7},
             {"name": "Detroit Red Wings", "abbreviation": "DET", "id": 17},
             {"name": "Ottawa Senators", "abbreviation": "OTT", "id": 9},
             {"name": "Montréal Canadiens", "abbreviation": "MTL", "id": 8},
             {"name": "Dallas Stars", "abbreviation": "DAL", "id": 25},
             {"name": "Winnipeg Jets", "abbreviation": "WPG", "id": 52},
             {"name": "Colorado Avalanche", "abbreviation": "COL", "id": 21},
             {"name": "Minnesota Wild", "abbreviation": "MIN", "id": 30},
             {"name": "Nashville Predators", "abbreviation": "NSH", "id": 18},
             {"name": "St. Louis Blues", "abbreviation": "STL", "id": 19},
             {"name": "Arizona Coyotes", "abbreviation": "ARI", "id": 53},
             {"name": "Chicago Blackhawks", "abbreviation": "CHI", "id": 16},
             {"name": "Vegas Golden Knights", "abbreviation": "VGK", "id": 54},
             {"name": "Seattle Kraken", "abbreviation": "SEA", "id": 55},
             {"name": "Edmonton Oilers", "abbreviation": "EDM", "id": 22},
             {"name": "Los Angeles Kings", "abbreviation": "LAK", "id": 26},
             {"name": "Calgary Flames", "abbreviation": "CGY", "id": 20},
             {"name": "Vancouver Canucks", "abbreviation": "VAN", "id": 23},
             {"name": "San Jose Sharks", "abbreviation": "SJS", "id": 28},
             {"name": "Anaheim Ducks", "abbreviation": "ANA", "id": 24}]
'''
await call.message.edit_text("<code>Загрузка...</code>")
team_id = call.data.split(":")[1]
url = 'https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"},{"property":"playerId","direction":"ASC"}]&start=0&limit=5&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId=' + str(
    team_id) + ' and gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023'
api_request(call.from_user.id, url)
querystring = {}
payload = ""
response = requests.request("GET", url, data=payload, params=querystring, timeout=3)
leaders_list = ""
for leader in json.loads(response.text)['data']:
    leaders_list = leaders_list + leader['lastName'] + " [" + str(leader['goals']) + "-" + str(
        leader['assists']) + "-" + str(leader['points']) + "]\n"
await call.message.edit_text("Лидеры <b>" + call.data.split(":")[2] + "</b>\n" + leaders_list)
'''
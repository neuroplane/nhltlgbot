import requests

url = 'https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"},{"property":"playerId","direction":"ASC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId=21 and gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023'

#url = "https://api.nhle.com/stats/rest/ru/skater/summary"

querystring = {}

payload = ""
response = requests.request("GET", url, data=payload, params=querystring)

print(response.text)
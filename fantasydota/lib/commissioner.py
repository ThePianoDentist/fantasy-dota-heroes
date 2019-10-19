import os

import json
import urllib2

from fantasydota.lib.constants import API_URL
from fantasydota.models import League

FE_APIKEY = os.environ.get("FE_APIKEY")
if not FE_APIKEY:
    print "Set your fantasy esport APIKEY environment variable"

filename = 'players_2019-07-15.json'#raw_input("players filename:")
with open(os.getcwd() + "/fantasydota/miscdata/" + filename) as f:
    teams = json.load(f)

def get_players(teams):
    pickees = []
    for team in teams:
        for player in team['players']:
            # player position and team name
            pickees.append({"id": player["account_id"], "name": player["name"], "value": 1.0, "limits": [player["position"], team['name']]})
    return pickees


def create_draft_league(session, commissioner_id, name, tournament_id, url, draft_start, choice_timer):

    periods = []
    for day in ([15, 16, 17, 18, 20, 21, 22, 23, 24, 25]):
        if day < 25:
            multiplier = 1.0
        else:
            multiplier = 2.0
        periods.append({'start': '2019-10-{} 00:00'.format(day), 'end': '2019-10-{} 00:00'.format(day+1), 'multiplier': multiplier})

    data = {
        'name': name,
        'apiKey': FE_APIKEY,
        'tournamentId': tournament_id,
        'gameId': 2,
        'pickeeDescription': 'Player',
        'periodDescription': 'Day',
        'startingMoney': 50.0,
        'teamSize': 5,
        'benchSize': 5,
        'transferInfo': {
            'system': 'draft',
            'draftStart': draft_start,
            'draftChoiceSecs': choice_timer,
            #'cardPackSize': 6,
            #'cardPackCost': 5,
            #'recycleValue': 0.2,
            #'predictionWinMoney': 2.0
        },
        "periods": periods,
        "url": url,
        "applyPointsAtStartTime": True,
        "limits": [{'name': 'position', 'types': [
            {'name': 'core', 'max': 2, 'benchMax': 2}, {'name': 'support', 'max': 2, 'benchMax': 2},
            {'name': 'offlane', 'max': 1, 'benchMax': 1},
        ]},
                   {'name': 'team', 'max': 2, 'types': [{'name': t['name']} for t in teams], 'benchMax': 2}
                   ],
        "stats": [
            #{'name': 'kills', 'allFactionPoints': 0.3},separateFactionPoints
            # {'name': 'deaths', 'allFactionPoints': -0.3},
            {'name': 'kills', 'separateFactionPoints': [
                {'name': 'support', 'value': 0.2}, {'name': 'offlane', 'value': 0.3}, {'name': 'core', 'value': 0.4}
            ]},
            {'name': 'assists', 'separateFactionPoints': [
                {'name': 'support', 'value': 0.1}, {'name': 'offlane', 'value': 0.1}, {'name': 'core', 'value': 0.05}
            ]},
            {'name': 'deaths', 'separateFactionPoints': [
                {'name': 'support', 'value': -0.2}, {'name': 'offlane', 'value': -0.2}, {'name': 'core', 'value': -0.5}
            ]},
            {'name': 'last hits', 'allFactionPoints': 0.003},
            {'name': 'denies', 'allFactionPoints': 0.003},
            {'name': 'GPM', 'description': 'Gold per Minute', 'allFactionPoints': 0.002},
            {'name': 'towers', 'description': 'Last hits on tower', 'allFactionPoints': 1.0},
            {'name': 'roshans', 'description': 'Last hits on roshan', 'allFactionPoints': 1.0},
            {'name': 'teamfight participation', 'allFactionPoints': 3.0},
            {'name': 'observer wards', 'allFactionPoints': 0.2},
            {'name': 'dewards', 'allFactionPoints': 0.25},
            {'name': 'camps stacked', 'allFactionPoints': 0.5},
            {'name': 'runes', 'description': 'Runes picked up', 'allFactionPoints': 0.25},
            {'name': 'first blood', 'allFactionPoints': 4.0},
            #{'name': 'stun', 'description': 'Number of seconds of stun applied to enemies', 'allFactionPoints': 0.05},
        ],
        'pickees': get_players(teams)
    }

    try:
        req = urllib2.Request(
            API_URL + "leagues/", data=json.dumps(data), headers={
                "Content-Type": "application/json"
            }
        )
        response = urllib2.urlopen(req).read()
        print(response)
        new_league = League(id=json.loads(response)["id"], name=name, commissioner=commissioner_id)
        session.add(new_league)
        return new_league
    except urllib2.HTTPError as e:
        print(e.read())
        raise
    # try:
    #     req = urllib2.Request(
    #         API_URL + "leagues/" + str(DEFAULT_LEAGUE), data=json.dumps({'transferOpen': True}), headers={
    #             "Content-Type": "application/json",
    #             "apiKey": FE_APIKEY
    #         }
    #     )
    #     response = urllib2.urlopen(req)
    #     print(response.read())
    # except urllib2.HTTPError as e:
    #     print(e.read())


    # req = urllib2.Request(
    #     API_URL + "leagues/1/startPeriod", data=json.dumps(data), headers={
    #         'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)',
    #         "Content-Type": "application/json"
    #     }
    # )
    # response = urllib2.urlopen(req)
    # print(response.read())

    # 16 * 5 = 80
    # 12 * 5 = 60
    # 8 * 5 = 40
import json
import os
import re
import time
import urllib2
import traceback

import transaction
from copy import copy
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Result, Match, League, ProCircuitTournament

APIKEY = os.environ.get("APIKEY")
if not APIKEY:
    print "Set your APIKEY environment variable"
LEAGUE_LISTING = "http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001?key=%s" % APIKEY


def dont_piss_off_valve_but_account_for_sporadic_failures(req_url):
    print("requesting {0}".format(req_url))
    fuck = True  # no idea why this failing. im waiting long enough to not piss off valve?
    sleep_time = 1
    fucks_given = 5
    while fuck and fucks_given:
        try:
            req = urllib2.Request(req_url, headers={'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)'})
            response = urllib2.urlopen(req)
            fuck = False
        except:
            sleep_time += 30  # incase script breaks dont want to spam
            print "Why the fuck are you fucking failing you fucker"
            traceback.print_exc()
            fucks_given -= 1
            time.sleep(sleep_time)
            continue
    data = json.load(response)
    return data


def get_league_match_list(league_id):
    return dont_piss_off_valve_but_account_for_sporadic_failures(
        "http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v0001?" \
        "key=%s&league_id=%s" % (APIKEY, league_id))


def get_match_details(match_id):
    return dont_piss_off_valve_but_account_for_sporadic_failures(
        "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v0001?" \
        "key=%s&match_id=%s" % (APIKEY, match_id))


def captains_draft(
        session, picks, add_match, match_json, radiant_win, week_id, tournament_id, match, series_id,
        set_applied_already
):
    if len(picks) < 16:
        print "MatchID: %s fucked up picks bans. not 22. Check if need update" % match
        return
    if add_match:
        day = session.query(League.current_day).filter(League.id == week_id).first()[0]
        try:
            session.add(Match(
                int(match_json["match_id"]), re.sub(r'\W+', '', match_json["radiant_name"]),
                re.sub(r'\W+', '', match_json["dire_name"]),
                match_json["radiant_win"], day, week_id, tournament_id
            ))
        except:
            print "Failed to add match: %s" % match_json["match_id"]
            return

    for key, value in enumerate(picks):
        key = int(key)

        if key <= 5:
            result_string = "b1"
        elif key <= 9:
            result_string = "p1"
            if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                result_string += "w"
            else:
                result_string += "l"
        elif key <= 13:
            result_string = "p2"
            if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                result_string += "w"
            else:
                result_string += "l"
        else:
            result_string = "p3"
            if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                result_string += "w"
            else:
                result_string += "l"
        print "Match is:", match_json["match_id"]
        # For if need to add results for calibration purposes. but dont want included in leagues
        if set_applied_already:
            session.add(Result(
                week_id, value["hero_id"], int(match_json["match_id"]), result_string,
                match_json["start_time"], series_id, (value["team"] == 0), match_json["start_time"],
                applied=2
            ))
        else:
            session.add(Result(
                week_id, value["hero_id"], int(match_json["match_id"]), result_string,
                match_json["start_time"], series_id, (value["team"] == 0), match_json["start_time"]
            ))


def add_matches(session, tournament_id, week_id=None, tstamp_from=0, add_match=True, set_applied_already=False):
    week_id = week_id or tournament_id
    match_list_json = get_league_match_list(tournament_id)

    matches = [(match["match_id"], match["series_id"]) for match in match_list_json["result"]["matches"]
               if match["start_time"] > tstamp_from and match["match_id"] != 3368387319]
    print "matches", matches
    for match, series_id in matches:
        with transaction.manager:
            if session.query(Result).filter(Result.match_id == match).first():  # if old result dont process
                continue

            match_json = get_match_details(match)["result"]
            radiant_win = match_json["radiant_win"]
            try:
                picks = match_json["picks_bans"]
            except KeyError:  # game crashed and they remade with all pick. need to manually
                print "MatchID: %s no picks and bans. Need manually inserting" % match
                continue
            if tournament_id == 5688:
                captains_draft(
                    session, picks, add_match, match_json, radiant_win, week_id, tournament_id, match, series_id,
                    set_applied_already
                )
            else:
                if len(picks) < 22:
                    print "MatchID: %s fucked up picks bans. not 22. Check if need update" % match
                    continue
                if add_match:
                    day = session.query(League.current_day).filter(League.id == week_id).first()[0]
                    try:
                        session.add(Match(
                            int(match_json["match_id"]), re.sub(r'\W+', '', match_json["radiant_name"]), re.sub(r'\W+', '', match_json["dire_name"]),
                            match_json["radiant_win"], day, week_id, tournament_id
                        ))
                    except:
                        print "Failed to add match: %s" % match_json["match_id"]
                        continue

                for key, value in enumerate(picks):
                    key = int(key)

                    if key <= 5:
                        result_string = "b1"
                    elif key <= 9:
                        result_string = "p1"
                        if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                            result_string += "w"
                        else:
                            result_string += "l"
                    elif key <= 13:
                        result_string = "b2"
                    elif key <= 17:
                        result_string = "p2"
                        if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                            result_string += "w"
                        else:
                            result_string += "l"
                    elif key <= 19:
                        result_string = "b3"
                    else:
                        result_string = "p3"
                        if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                            result_string += "w"
                        else:
                            result_string += "l"
                    print "Match is:", match_json["match_id"]
                    # For if need to add results for calibration purposes. but dont want included in leagues
                    if set_applied_already:
                        session.add(Result(
                            week_id, value["hero_id"], int(match_json["match_id"]), result_string,
                            match_json["start_time"], series_id, (value["team"] == 0), match_json["start_time"],
                            applied=2
                        ))
                    else:
                        session.add(Result(
                            week_id, value["hero_id"], int(match_json["match_id"]), result_string,
                            match_json["start_time"], series_id, (value["team"] == 0), match_json["start_time"]
                        ))
    transaction.commit()


def main():
    session = make_session()
    #session2 = make_session(False)
    # dreamleague calibration
    game_id = 1
    try:
        set_applied_already = False
        week_id = session.query(League.id).filter(League.game == game_id).filter(League.status == 1).first()[0]
    except:
        set_applied_already = True
        week_id = session.query(League.id).filter(League.game == game_id).filter(League.status == 0).first()[0]
    #tournaments = [x[0] for x in session.query(ProCircuitTournament.id).all()]
    # PRO_CIRCUIT_LEAGUES = [
    #     {'id': 5627, 'name': 'Dreamleague 8', 'major': True},
    #     {'id': 5850, 'name': 'Summit 8', 'major': False},
    #     {'id': 5688, 'name': 'Captains Draft 4', 'major': False},
    #     {'id': 5504, 'name': 'MDL Macau', 'major': False},
    #     {'id': 5637, 'name': 'Perfect World Master', 'major': False},
    # ]
    # tournaments.extend([x['id'] for x in PRO_CIRCUIT_LEAGUES])
    #tournaments.extend([5562, 9579, 8055, 5572, 5616, 9579, 5562, 5651, 4820])
    tournaments = [10145, 5562, 10087, 9836, 4127, 10061]  # TI8 calibration tournaments
    for tournament in list(set(tournaments)):
        add_matches(session, tournament, tstamp_from=1511806059, week_id=week_id,
                    set_applied_already=set_applied_already)

if __name__ == "__main__":
    main()

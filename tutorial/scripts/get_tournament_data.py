import json
import os
import time
import urllib2

import transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from tutorial import Base
from tutorial.lib.session_utils import make_session
from tutorial.models import Result
from zope.sqlalchemy import ZopeTransactionExtension

APIKEY = os.environ.get("APIKEY")
if not APIKEY:
    print "Set your APIKEY environment variable"
LEAGUE_LISTING = "http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001?key=%s" % APIKEY


def dont_piss_off_valve_but_account_for_sporadic_failures(req_url):
    fuck = True  # no idea why this failing. im waiting long enough to not piss off valve?
    sleep_time = 5  # valve say no more than 1 per second. be safe
    while fuck:
        try:
            response = urllib2.urlopen(req_url)
            fuck = False
        except:
            sleep_time += 30  # incase script breaks dont want to spam
            print "Why the fuck are you fucking failing you fucker"
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


def add_matches(session):
    tournament_id = 4874  # Boston major
    match_list_json = get_league_match_list(tournament_id)

    matches = [(match["match_id"], match["series_id"]) for match in match_list_json["result"]["matches"]
               if match["start_time"] > 1481193665]
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
            if len(picks) < 16:  # theres some weird buggy matches in there
                print "MatchID: %s fucked up picks bans. Check if should be added" % match
                continue
            elif len(picks) < 20:
                print "MatchID: %s fucked up picks bans. not 20. Check if need update" % match
                continue
            for key, value in enumerate(picks):
                key = int(key)

                if key <= 3:
                    result_string = "b1"
                elif key <= 7:
                    result_string = "p1"
                    if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                        result_string += "w"
                    else:
                        result_string += "l"
                elif key <= 11:
                    result_string = "b2"
                elif key <= 15:
                    result_string = "p2"
                    if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                        result_string += "w"
                    else:
                        result_string += "l"
                elif key <= 17:
                    result_string = "b3"
                else:
                    result_string = "p3"
                    if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                        result_string += "w"
                    else:
                        result_string += "l"
                print "Match is:", match_json["match_id"]
                session.add(Result(tournament_id, value["hero_id"], int(match_json["match_id"]), result_string,
                                   match_json["start_time"], series_id))
    transaction.commit()


def main():
    session = make_session()
    add_matches(session)

if __name__ == "__main__":
    main()

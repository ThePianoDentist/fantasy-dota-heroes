import csv

from fantasydota.lib.constants import DIR
from fantasydota.lib.herolist import heroes
from fantasydota.models import Hero, Result
from sqlalchemy import and_
from sqlalchemy import func


def manual_overrides(hero_list):
    treant = [hero for hero in hero_list if hero["name"] == "Treant Protector"][0]
    treant["value"] = 20.0
    underlord = [hero for hero in hero_list if hero["name"] == "Underlord"][0]
    underlord["value"] = 14.0
    return hero_list

def squeeze_values_together(hero_list):
    # this is for if unsure and would rather have things have averagish values rather than exremes
    average_value = sum([hero["value"] for hero in hero_list])/ len(hero_list)
    for hero in hero_list:
        hero["value"] -= ((hero["value"] - average_value) / 4.)
        hero["value"] = round(hero["value"], 1)
        print "New %s: %s" % (hero["name"], hero["value"])

    return hero_list


def calibrate_all_hero_values_datdota(session, patch=None):
    # Technically because I give extra points for 3rd phase wins
    # and in dat dota its only fixed winrate across all pick stages
    # but making smart sales is still fun.
    # im not ure calibration needs to be so accurate
    with open(DIR + '/fantasydota/junk/%s.csv' % patch, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        ddota_heroes = []
        new_heroes_list = heroes
        for h in new_heroes_list:
            h["points"] = 0
        sum_points = 0
        for i, row in enumerate(readCSV):
            if i == 0:
                continue
            if "echies" in row[0]:
                continue
            h_dict = {
                "name": row[0],
                "phase_one_pick": float(row[3]),
                "phase_two_pick": float(row[4]),
                "phase_three_pick": float(row[5]),
                "pick_win_percent": float(row[6].replace("%", "").replace("?", "0")),
                "phase_one_ban": float(row[9]),
                "phase_two_ban": float(row[10]),
                "phase_three_ban": float(row[11]),
                "total_ban": float(row[12]),
                "total_picks": float(row[7])
            }

            ddota_heroes.append(h_dict)

            points = h_dict["phase_one_pick"] * 2 + h_dict["phase_two_pick"] * 3 + h_dict["phase_three_pick"] * 5 + \
                     h_dict["phase_one_ban"] + h_dict["phase_two_ban"] * 2 + h_dict["phase_three_ban"] * 4 + h_dict["pick_win_percent"] * 8/100. * h_dict["total_picks"] -\
                ((100 - h_dict["pick_win_percent"]) * 6/100. * h_dict["total_picks"])
            print h_dict["name"], ": ", points
            try:
                h_dict["name"] = h_dict["name"].replace("indrunner", "indranger").replace("ecrolyte", "ecrophos").replace("Abyssal", "").replace("thrope", "")
                [hero for hero in new_heroes_list if ''.join([i for i in hero["name"].lower() if i.isalpha()]) == ''.join([i for i in h_dict["name"].lower() if i.isalpha()])][0]["points"] += points
            except:
                raise
            sum_points += points
        average_points = sum_points / len(new_heroes_list)
        sum = 0
        i = 0
        for hero in new_heroes_list:
            if hero["points"] < 0:
                hero["points"] = 1
            value = calibrate_value(average_points, hero["points"])
            for hero_d in new_heroes_list:
                if hero_d["id"] == hero["id"]:
                    hero_d["value"] = round(value, 1)
                    print "New %s: %s" % (hero_d["name"], round(value, 1))
            sum += value
            i += 1
        print "Average new value:", sum / i
        return new_heroes_list

def calibrate_all_hero_values(session, patch=None):
    new_heroes_list = heroes
    for h in new_heroes_list:
        h["points"] = 0
    if patch:
        start_time, end_time = get_patch_timestamps(patch)
        results = session.query(Result).filter(Result.applied.is_(False)).\
            filter(Result.timestamp > start_time).filter(Result.timestamp < end_time).all()
    else:
        results = session.query(Result).filter(Result.applied.is_(False)).all()
    sum_points = 0

    for res in results:
        points = Result.result_to_value(res.result_str)
        [hero for hero in new_heroes_list if hero["id"] == res.hero][0]["points"] += points
        sum_points += points
    average_points = sum_points / len(new_heroes_list)
    sum = 0
    i = 0
    for hero in new_heroes_list:
        if hero["points"] < 0:
            hero["points"] = 1
        value = calibrate_value(average_points, hero["points"])
        for hero_d in new_heroes_list:
            if hero_d["id"] == hero["id"]:
                hero_d["value"] = round(value, 1)
                print "New %s: %s" % (hero_d["name"], round(value, 1))
        sum += value
        i += 1
    print "Average new value:", sum / i
    return new_heroes_list


def write_calibration(new_heroes_list):
    "/home/jdog/bin/seovenv/bin/fantasydota/fantasydota/lib/herolist_vals.py"
    with open("/home/jdog/projects/fantasy-dota-heroes/fantasydota/lib/herolist_vals.py", 'w+') as f:
        f.write("heroes_init = " + repr(new_heroes_list))


def calibrate_value(average_points, our_points):
    output = ((float(our_points) / float(average_points)) * 9.0 * 3 + 9.0) / 4.
    if output < 1.0:  # dont get into negative price shenanigans
        output = 1.0
    return output


def combine_calibrations(older_value, newer_value):
    return (newer_value + older_value * 4) / 5.


def recalibrate_hero_values(session, league_id):
    heroes = session.query(Hero).filter(Hero.league == league_id)
    average_points = float(session.query(func.avg(Hero.points)).filter(Hero.league == league_id).scalar())
    for hero in heroes:
        new_calibration = calibrate_value(average_points, hero.points)
        print "new calbration: %s, from %s" % (new_calibration, hero.value)
        hero.value = round(combine_calibrations(hero.value, new_calibration), 1)

import datetime

import random
from passlib.handlers.bcrypt import bcrypt
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden)
from pyramid.security import (
    remember,
    forget,
    authenticated_userid)
from pyramid.view import (
    view_config,
)
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import or_
from fantasydota.lib.battlecup import check_winner_exists, fight
from fantasydota.lib.herolist_vals import heroes_init
from fantasydota.util.random_function import add_months, bprint

from fantasydota.models import (
    DBSession,
    User, Hero, TeamHeroLeague, Friend, Result, BattlecupUser, Battlecup, UserLeague, League)


@view_config(route_name='view_faq', renderer='../templates/view_faq.mako')
def view_faq(request):
    return {}


@view_config(route_name='view_rules', renderer='../templates/view_rules.mako')
def view_rules(request):
    return {}


@view_config(route_name='view_index')
def view_index(request):
    return HTTPFound("/viewLeague?league=4874")


@view_config(route_name='view_account', renderer='../templates/view_account.mako')
def view_account(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        return HTTPFound('/login')
    return HTTPFound("/viewLeague?league=4874")


@view_config(route_name='leaderboard', renderer='../templates/view_leaderboard.mako')
def leaderboard(request):
    session = DBSession()
    user = authenticated_userid(request)

    show_friend = True if request.params.get("showFriend") and user else False
    if show_friend:
        switch_to = "global"
        friends = [kek[0] for kek in session.query(Friend.friend).filter(Friend.user == user).all()]
    else:
        switch_to = "friend"
    period = request.params.get("period")
    if not period:
        period = "tournament"

    rank_by = request.params.get("rank_by")
    if rank_by not in ("points", "wins", "picks", "bans"):
        rank_by = "points"

    # should prob move this func
    def rank_filter(rank_by, period):
        userOb = User if period == "tournament" else HistoryUser
        if rank_by == "wins":
            return userOb.wins
        elif rank_by == "picks":
            return userOb.picks
        elif rank_by == "bans":
            return userOb.bans
        else:
            return userOb.points

    def period_filter(period):
        if period == "day1":
            return "2016-12-04"
        elif period == "day2":
            return "2016-12-05"
        elif period == "day3":
            return "2016-12-08"
        elif period == "day4":
            return "2016-12-09"
        elif period == "day5":
            return "2016-12-10"
        elif period == "day6":
            return "2016-12-11"

    rank_ = rank_filter(rank_by, period)
    period_ = period_filter(period)

    player_heroes = []
    if period == "tournament":
        user = session.query(User).filter(User.username == user).first()
        if show_friend:
            players = session.query(User).filter(or_(User.username.in_(friends), User.username == user)).\
                order_by(desc(rank_)).limit(100).all()
        else:
            players = session.query(User).order_by(desc(rank_)).limit(100).all()

        if not request.registry.settings["transfers"]:
            for player in players:
                heroes = []
                for hero in session.query(TeamHero).filter(and_(TeamHero.user == player.username,
                                                                TeamHero.active == True)).all():
                    heroes.append(session.query(Hero.name).filter(Hero.hero_id == hero.hero).first()[0])
                player_heroes.append(heroes)
    else:
        user = session.query(HistoryUser).filter(and_(HistoryUser.username == user, HistoryUser.date == period_)).first()
        if show_friend and user:
            players = session.query(HistoryUser).filter(HistoryUser.date == period_).\
                filter(or_(HistoryUser.username.in_(friends), HistoryUser.username == user)).\
                order_by(desc(rank_)).limit(100).all()
        else:
            players = session.query(HistoryUser).filter(HistoryUser.date == period_).\
                order_by(desc(rank_)).limit(100).all()
        for player in players:
            heroq = [player.hero_one, player.hero_two, player.hero_three, player.hero_four, player.hero_five]
            heroq = [hero for hero in heroq if hero != 0]
            heroes = [session.query(Hero.name).filter(Hero.hero_id == hero).first()[0] for hero in heroq]
            player_heroes.append(heroes)

    return {'user': user, 'players': players, 'rank_by': rank_by, 'switch_to': switch_to, 'period': period,
            'player_heroes': player_heroes}


# @view_config(route_name='battlecup_json', renderer='json')
# def battlecup_json(request):
#     session = DBSession()
#     battlecup_round = session.query(Battlecup.last_completed_round).first()[0]
#     battlecup_id = request.params.get("battlecup_id")
#     battlecup = session.query(BattlecupUserPoints).filter(and_(BattlecupUserPoints.battlecup_id == battlecup_id,
#                                                                BattlecupUserPoints.date > 100)).\
#         order_by(BattlecupUserPoints.username).order_by(BattlecupUserPoints.series_id).all()
#
#     player_q = session.query(BattlecupUser).filter(BattlecupUser.battlecup_id == battlecup_id).\
#         group_by(BattlecupUser.username).order_by(BattlecupUser.username)
#
#     player_names, hero_imgs = [], []
#
#     class FakePlayer(object):
#         def __init__(self):
#             self.username = None
#             self.points = -9000
#
#     fake_player = FakePlayer()
#     # Hack to have a bye for the missing 8th player
#
#     num_players = player_q.count()
#
#     if battlecup_round <= 1:
#         results = []
#         players = player_q.all()
#         if num_players == 7:
#             players.append(fake_player)
#         for i in range(0, len(players), 2):
#             pname1, pname2 = players[i].username.title(), players[i+1].username.title()
#             player_names.append([pname1, pname2])
#
#             hero_ids = [res[0] for res in
#                         session.query(TeamHero.hero).filter(and_(TeamHero.user == players[i].username,
#                                                                  TeamHero.active == True)).all()]
#             player1_heronames = {"pname": pname1,
#                                  "heroes": [hDict["name"].replace(" ", "_") for hDict in heroes_init if hDict["id"] in hero_ids
#                                             ]}
#             hero_ids = [res[0] for res in
#                         session.query(TeamHero.hero).filter(and_(TeamHero.user == players[i+1].username,
#                                                                  TeamHero.active == True)).all()]
#             player2_heronames = {"pname": pname2,
#                                  "heroes": [hDict["name"].replace(" ", "_") for hDict in heroes_init if hDict["id"] in
#                                             hero_ids
#                                             ]}
#             hero_imgs.extend([player1_heronames, player2_heronames])
#
#     else:
#         players = [[],[],[],[],[],[],[],[]]
#         for i, pres in enumerate(battlecup):
#             print i, pres
#             players[i/(len(battlecup) / num_players)].append(pres)
#
#         if num_players == 7:
#             players[7] = [fake_player]
#
#         round_zero_points, round_one_points, round_two_points = [], [], []
#
#         if battlecup_round > 1:
#             for i in range(0, len(players), 2):
#                 player1, player2 = players[i][0], players[i+1][0]
#                 p1_points, p2_points = check_winner_exists(session, player1, player2)
#                 round_zero_points.append([p1_points, p2_points])
#
#                 pname1, pname2 = players[i][0].username.title(), players[i+1][0].username.title()
#                 player_names.append([pname1, pname2])
#
#                 hero_ids = [res[0] for res in session.query(TeamHero.hero).filter(and_(TeamHero.user == players[i][0].username),
#                                                                                        TeamHero.active == True).all()]
#                 player1_heronames = {"pname": pname1,
#                                      "heroes": [hDict["name"].replace(" ", "_") for hDict in heroes_init if hDict["id"] in hero_ids
#                                      ]}
#                 hero_ids = [res[0] for res in
#                             session.query(TeamHero.hero).filter(and_(TeamHero.user == players[i+1][0].username),
#                                                                 TeamHero.active == True).all()]
#                 player2_heronames = {"pname": pname2,
#                                      "heroes": [hDict["name"].replace(" ", "_") for hDict in heroes_init if hDict["id"] in
#                                                 hero_ids
#                                      ]}
#                 hero_imgs.extend([player1_heronames, player2_heronames])
#
#         if battlecup_round > 2:
#             next_round_players = fight(players, 0)[0]
#             for i in range(0, len(next_round_players), 2):
#                 player1, player2 = next_round_players[i][1], next_round_players[i + 1][1]
#                 p1_points, p2_points = check_winner_exists(session, player1, player2)
#                 round_one_points.append([p1_points, p2_points])
#
#         if battlecup_round > 3:
#             next_round_players, third_place_playoffs = fight(next_round_players, 1)
#             for i in range(0, len(next_round_players), 2):
#                 player1, player2 = next_round_players[i][2], next_round_players[i + 1][2]
#                 player3, player4 = third_place_playoffs[i][2], third_place_playoffs[i + 1][2]
#                 p1_points, p2_points = check_winner_exists(session, player1, player2)
#                 p3_points, p4_points = check_winner_exists(session, player3, player4)
#                 round_two_points.append([p1_points, p2_points])
#                 round_two_points.append([p3_points, p4_points])
#
#         results = []
#         if battlecup_round > 0:
#             results.append(round_zero_points)
#         if battlecup_round > 1:
#             results.append(round_one_points)
#         if battlecup_round > 2:
#             results.append(round_two_points)
#
#     bracket_dict = {
#         "teams": player_names,
#         "results": results
#     }
#
#     return {"bracket_dict": bracket_dict, "hero_imgs": hero_imgs}


@view_config(route_name='login', renderer='../templates/login.mako')
def login(request):
    session = DBSession()
    message = request.params.get('message')
    username = request.params.get('username')
    if request.method == 'POST':
        if username:
            username = username.lower()
            userq = session.query(User).filter(User.username == username)
            user = userq.first()
            if user:
                if user.validate_password(request.params.get('password')):
                    headers = remember(request, user.username)
                    userq.update({User.last_login: datetime.datetime.now()})
                    return HTTPFound('/viewLeague?league=4874', headers=headers)
                else:
                    headers = forget(request)
                    message = "Password did not match stored value for %s" % user.username
            else:
                message = "Username not recognised"
        else:
            message = 'Oops! SOmething went wrong'
            headers = forget(request)
    return {'message': message}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)


@view_config(route_name='register')
def register(request):
    session = DBSession()
    username = request.params.get('username').lower()
    password = request.params.get('password')
    email = request.params.get('email')
    if len(username) < 3:
        params = {"message": "Username too short"}
        return HTTPFound(location=request.route_url('login', _query=params))
    elif len(username) > 20:
        params = {"message": "Username too long (20 characters max)"}
        return HTTPFound(location=request.route_url('login', _query=params))
    if len(password) < 6:
        params = {"message": "Password too short. 6 characters minimum please"}
        return HTTPFound(location=request.route_url('login', _query=params))
    elif len(password) > 20:
        params = {"message": "Password too long. 20 characters maximum please"}
        return HTTPFound(location=request.route_url('login', _query=params))
    elif not username.replace(" ", "").isalnum():
        params = {"message": "Only letters and numbers in username please."}
        return HTTPFound(location=request.route_url('login', _query=params))
    confirm_password = request.params.get('confirm_password')
    user = session.query(User).filter(User.username == username).first()
    if not user:
        if confirm_password != password:
            params = {"message": "Passwords did not match"}
            return HTTPFound(location=request.route_url('login', _query=params))
        user = User(username, password, email)
        session.add(user)
        leagues = session.query(League).all()
        for l in leagues:
            user_league = UserLeague(username, l.id)
            session.add(user_league)
        headers = remember(request, user.username)
        return HTTPFound('/viewLeague?league=4874', headers=headers)
    else:
        params = {"message": "Username already in use"}
        return HTTPFound(location=request.route_url('login', _query=params))


@view_config(route_name='change_password')
def change_password(request):
    session = DBSession()
    username = authenticated_userid(request)
    new_password = request.params.get('new_password')
    confirm_new_password = request.params.get('confirm_new_password')
    old_password = request.params.get('old_password')
    user = session.query(User).filter(User.username == username).first()
    if not user:
        params = {"message": "Your username could not be found",
                  "message_type": "change_password"}
        return HTTPFound(location=request.route_url('viewAccount', _query=params))
    if confirm_new_password != new_password:
        params = {"message": "Passwords did not match",
                  "message_type": "change_password"}
        return HTTPFound(location=request.route_url('viewAccount', _query=params))
    if not user.validate_password(old_password):
        params = {"message": "Old password did not match",
                  "message_type": "change_password"}
        return HTTPFound(location=request.route_url('viewAccount', _query=params))

    if len(new_password) < 6:
        params = {"message": "Password too short. 6 characters minimum please"}
        return HTTPFound(location=request.route_url('viewAccount', _query=params))
    elif len(new_password) > 20:
        params = {"message": "Password too long. 20 characters maximum please"}
        return HTTPFound(location=request.route_url('viewAccount', _query=params))
    session.query(User).filter(User.username == username).update({User.password: bcrypt.encrypt(new_password)})
    params = {"message": "Congratulations! Password successfully changed",
                  "message_type": "change_password_success"}
    return HTTPFound(location=request.route_url('viewAccount', _query=params))


@view_config(route_name='account_settings', renderer="../templates/view_account_settings.mako")
def account_settings(request):
    return {}

# @view_config(route_name='email_test')
# def email_test(request):
#     # python -m smtpd -n -c DebuggingServer localhost:2525
#     message = Message(subject="hello world",
#                       sender="seoranktrack@gmail.com",
#                       recipients=["jbknight07@gmail.com"],
#                       body="hello, arthur")
#     mailer = get_mailer(request)
#     mailer.send(message)
#     return HTTPFound('/')


@view_config(route_name="add_friend", renderer="json")
def add_friend(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()

    new_friend = request.POST["newFriend"].lower()
    if session.query(Friend).filter(and_(Friend.user == user, Friend.friend == new_friend)).first():
        return {"success": False, "message": "You have already added that friend"}
    else:
        session.add(Friend(user, new_friend))
        return {"success": True, "message": "Friend successfully added"}


@view_config(route_name="switch_transfers", renderer="string")
def switch_transfers(request):
    change = request.params.get("state")
    if request.remote_addr not in ('127.0.0.1', '149.210.217.128'):
        raise HTTPForbidden()
    bprint(request.remote_addr)
    if change == 'open':
        request.registry.settings.update({"transfers": True})
        return "transfer window opened"
    elif change == 'closed':
        request.registry.settings.update({"transfers": False})
        return "transfer window closed"
    else:
        return "incorrect state param"


@view_config(route_name="news", renderer="../templates/news.mako")
def news(request):
    return {}

def get_time_range(time_range):
    if time_range == 'week':
        date_start = datetime.datetime.now() - datetime.timedelta(days=7)
        date_end = datetime.datetime.now()
    elif time_range == 'month':
        date_start = add_months(datetime.datetime.now(), -1)
        date_end = datetime.datetime.now()
    else:
        date_start = datetime.datetime(2015, 11, 1)
        date_end = datetime.datetime.now()
    return date_start, date_end

import transaction
# from sqlalchemy import and_
# from sqlalchemy import desc
from sqlalchemy import and_

from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, Result, TeamHero, LeagueUser, Sale


#
#
#
def add_hero_player(session, user_id, hero_id, league_id):
    with transaction.manager:

        hero_value = session.query(Hero.value).filter(and_(Hero.id == hero_id,
                                                           Hero.league == league_id)).first()[0]

        teamq = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id)
        teamq_hero = teamq.filter(TeamHero.hero_id == hero_id)

        l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).filter(
            LeagueUser.league == league_id).first()

        user_money = l_user.money

        if user_money < hero_value:
            return {"success": False, "message": "ERROR: Insufficient credits"}

        new_credits = round(user_money - hero_value, 1)

        if teamq.count() >= 5:
            return {"success": False, "message": "ERROR: Team is currently full"}
        if teamq_hero.first():
            return {"success": False, "message": "ERROR: Hero already in team"}
        else:
            l_user.money = new_credits
            session.add(TeamHero(user_id, hero_id, league_id, hero_value))
            session.add(Sale(l_user.id, hero_id, league_id, hero_value, hero_value, True))

        transaction.commit()


def main():
    session = make_session()
    add_hero_player(session, 507, 78, 5401)
    add_hero_player(session, 507, 104, 5401)

if __name__ == "__main__":
    main()

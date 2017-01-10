import os

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.exc import DisconnectionError
from fantasydota.scripts.init_tables import create_tables
from fantasydota.util.jsonhelpers import custom_json_renderer

from .models import (
    Base,
    DBSession)


# I was getting 2006 mysql gone away if website left for few hours. didnt know why
def checkout_listener(dbapi_con, con_record, con_proxy):
    try:
        try:
            dbapi_con.ping(False)
        except TypeError:
            dbapi_con.ping()
    except dbapi_con.OperationalError as exc:
        if exc.args[0] in (2006, 2013, 2014, 2045, 2055):
            raise DisconnectionError()
        else:
            raise


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings["league_transfers"] = True  # why wont config file properly set this?
    settings["default_league"] = 5018
    sqlalchemy_url = os.path.expandvars(settings.get('sqlalchemy.url')) + "2"
    engine = create_engine(sqlalchemy_url, echo=False, pool_size=100, pool_recycle=3600)
    event.listen(engine, 'checkout', checkout_listener)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    create_tables(DBSession)

    # Need https set up on local machine for secure True to work locally
    authn_policy = AuthTktAuthenticationPolicy('sosecret', hashalg='sha512', http_only=True)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, authentication_policy=authn_policy,
        authorization_policy=authz_policy,)

    config.include('pyramid_mako')
    config.include('pyramid_mailer')
    config.add_renderer('json', custom_json_renderer())
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('view_index', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('view_faq', '/faq')
    config.add_route('view_rules', '/rules')
    config.add_route('view_account', '/viewAccount')
    config.add_route('view_league', '/viewLeague')
    config.add_route('register', '/register')
    config.add_route('change_password', '/changePassword')
    config.add_route('forgot_password', '/forgotPassword')
    config.add_route('reset_password', '/resetPassword')
    config.add_route('reset_password_page', '/resetPasswordPage')
    config.add_route('update_email_settings', '/updateEmailSettings')
    config.add_route('update_game_settings', '/gameSettings')

    config.add_route("add_friend", '/addFriend')
    config.add_route('trade_shares', '/tradeShares')
    config.add_route('buy_hero_battlecup', '/buyHeroBcup')
    config.add_route('sell_hero_battlecup', '/sellHeroBcup')
    config.add_route('buy_hero_league', '/buyHeroLeague')
    config.add_route('sell_hero_league', '/sellHeroLeague')
    config.add_route('leaderboard', '/leaderboard')
    config.add_route('switch_transfers', '/tran012345678901234567890looptheloop')
    config.add_route('account_settings', '/accountSettings')
    config.add_route('news', '/news')
    config.add_route('hall_of_fame', '/hallOfFame')
    config.add_route('battlecup', '/battlecup')
    config.add_route('battlecup_team', '/battlecupTeam')
    config.add_route('battlecup_json', '/battlecupJson')
    config.add_route('battlecup_add_league_team', '/bcupTeamAddLeague')
    config.add_route('battlecup_add_yesterday_team', '/bcupTeamAddYesterday')
    config.scan()
    return config.make_wsgi_app()

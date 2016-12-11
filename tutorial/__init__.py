import os

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import create_engine
from sqlalchemy.exc import DisconnectionError
from tutorial.scripts.init_tables import create_tables
from tutorial.util.jsonhelpers import custom_json_renderer

from .models import (
    Base,
    Root, DBSession)


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
    settings["transfers"] = True  # why wont config file properly set this?
    sqlalchemy_url = os.path.expandvars(settings.get('sqlalchemy.url'))
    engine = create_engine(sqlalchemy_url, echo=False, pool_size=100, pool_recycle=3600)
    #event.listen(engine, 'checkout', checkout_listener)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    create_tables(DBSession)

    authn_policy = AuthTktAuthenticationPolicy('sosecret', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, authentication_policy=authn_policy,
        authorization_policy=authz_policy,)

    config.include('pyramid_mako')
    config.include('pyramid_mailer')
    config.add_renderer('json', custom_json_renderer())
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('view_faq', '/faq')
    config.add_route('view_rules', '/rules')
    config.add_route('view_account', '/view_account')
    config.add_route('register', '/register')
    config.add_route('change_password', '/change_password')

    config.add_route("add_friend", '/addFriend')
    config.add_route('trade_shares', '/tradeShares')
    config.add_route('buy_hero', '/buyHero')
    config.add_route('sell_hero', '/sellHero')
    config.add_route('leaderboard', '/leaderboard')
    config.add_route('switch_transfers', '/tran012345678901234567890looptheloop')
    config.add_route('account_settings', '/accountSettings')
    config.add_route('news', '/news')
    config.add_route('battlecup', '/battlecup')
    config.add_route('battlecup_json', '/battlecup_json')
    config.scan()
    return config.make_wsgi_app()

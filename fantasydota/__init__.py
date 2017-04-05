import os

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from social_pyramid.models import init_social
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.exc import DisconnectionError

import local_settings as app_local_settings
import settings as app_settings
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


def get_settings(module):
    return { key: value for key, value in module.__dict__.items()
              if key not in module.__builtins__ and
                 key not in ['__builtins__', '__file__'] }


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings["league_transfers"] = True  # why wont config file properly set this?
    settings["default_league"] = 5157
    sqlalchemy_url = os.path.expandvars(settings.get('sqlalchemy.url')) 
    engine = create_engine(sqlalchemy_url, echo=False, pool_size=100, pool_recycle=3600)
    event.listen(engine, 'checkout', checkout_listener)
    DBSession.configure(bind=engine)

    # Need https set up on local machine for secure True to work locally
    authn_policy = AuthTktAuthenticationPolicy(settings.get('authn_policy_secr'), hashalg='sha512', http_only=True,
                                               max_age=10000000)
    authz_policy = ACLAuthorizationPolicy()

    my_session_factory = session_factory_from_settings(settings)
    # my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet', cookie_max_age=10000000,
    #                                                            cookie_httponly=True)

    config = Configurator(settings=settings, session_factory=my_session_factory, authentication_policy=authn_policy,
        authorization_policy=authz_policy,)

    config.add_route('home', '/')
    config.add_route('done', '/done')

    config.registry.settings.update(get_settings(app_settings))
    config.registry.settings.update(get_settings(app_local_settings))

    init_social(config, Base, DBSession)  # is this the right place?
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    #create_tables(DBSession) already created!

    config.include('social_pyramid')
    config.scan('social_pyramid')

    # pyramid_social_auth.register_provider(settings, google.GoogleOAuth2)
    # psa.register_provider(settings, facebook.FacebookOAuth2)

    config.add_request_method('.auth.get_user', 'user', reify=True)  # user or username? should it start with .?

    config.add_renderer('json', custom_json_renderer())
    config.add_static_view('static', 'static', cache_max_age=3600)
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

    config.add_route("add_friend", '/addFriend')
    config.add_route('buy_hero', '/buyHero')
    config.add_route('sell_hero', '/sellHero')
    config.add_route('leaderboard', '/leaderboard')
    config.add_route('account_settings', '/accountSettings')
    config.add_route('news', '/news')
    config.add_route('hall_of_fame', '/hallOfFame')
    config.add_route('guess_hero', 'guessHero')
    config.scan()
    return config.make_wsgi_app()

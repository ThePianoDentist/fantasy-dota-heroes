from uuid import uuid4

from social_core.pipeline.user import USER_FIELDS
from social_core.utils import module_member, slugify

from fantasydota.lib.constants import OTHER_ACCOUNT, SOCIAL_CODES
from fantasydota.views.account_views import logout


def check_invalid_password(password, confirm_password):
    if len(password) < 6:
        return {"message": "Password too short. 6 characters minimum please"}
    elif len(password) > 20:
        return {"message": "Password too long. 20 characters maximum please"}
    elif confirm_password != password:
        return{"message": "Passwords did not match"}
    else:
        return False


def get_non_unique_username(strategy, details, backend, user=None, *args, **kwargs):
    """
    override the python social auth method, as I dont want to follow the enforcing unique username strategy
    :param strategy:
    :param details:
    :param backend:
    :param user:
    :param args:
    :param kwargs:
    :return:
    """
    if 'username' not in backend.setting('USER_FIELDS', USER_FIELDS):
        return
    storage = strategy.storage

    if not user:
        email_as_username = strategy.setting('USERNAME_IS_FULL_EMAIL', False)
        uuid_length = strategy.setting('UUID_LENGTH', 16)
        max_length = storage.user.username_max_length()
        do_slugify = strategy.setting('SLUGIFY_USERNAMES', False)
        do_clean = strategy.setting('CLEAN_USERNAMES', True)

        if do_clean:
            override_clean = strategy.setting('CLEAN_USERNAME_FUNCTION')
            if override_clean:
                clean_func = module_member(override_clean)
            else:
                clean_func = storage.user.clean_username
        else:
            clean_func = lambda val: val

        if do_slugify:
            override_slug = strategy.setting('SLUGIFY_FUNCTION')
            if override_slug:
                slug_func = module_member(override_slug)
            else:
                slug_func = slugify
        else:
            slug_func = lambda val: val

        if email_as_username and details.get('email'):
            username = details['email']
        elif details.get('username'):
            username = details['username']
        else:
            username = uuid4().hex
        final_username = slug_func(clean_func(username[:max_length]))

        # Generate a unique username for current user using username
        # as base but adding a unique hash at the end. Original
        # username is cut to avoid any field max_length.
        # The final_username may be empty and will skip the loop.
        # while not final_username or \
        #       storage.user.user_exists(username=final_username):
        #     username = short_username + uuid4().hex[:uuid_length]
        #     final_username = slug_func(clean_func(username[:max_length]))
    else:
        final_username = storage.user.get_username(user)
    return {'username': final_username}


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}
    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    fields['account_type'] = SOCIAL_CODES.get(backend.name, OTHER_ACCOUNT)
    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
}

def social_user(backend, uid, user=None, *args, **kwargs):
    '''OVERRIDED: It will logout the current user
    instead of raise an exception '''

    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            print('This {0} account is already in use.'.format(provider))
            logout(backend.strategy.request)
            #msg = 'This {0} account is already in use.'.format(provider)
            #raise AuthAlreadyAssociated(backend, msg)
        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}
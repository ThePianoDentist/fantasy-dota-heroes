import datetime

import urllib2

import json
from fantasydota.lib.constants import DEFAULT_LEAGUE, API_URL
from fantasydota.models import Notification, User
from pyramid.security import authenticated_userid
from sqlalchemy import desc


def add_notifications(return_dict, session, user_id):
    notifications = session.query(Notification).filter(Notification.user == user_id)\
        .filter(Notification.seen.is_(False)).order_by(desc(Notification.id)).limit(10).all()
    return_dict['notifications'] = notifications
    return return_dict


def all_view_wrapper(return_dict, session, user_id=None):
    return_dict['user_id'] = user_id
    return_dict['user'] = session.query(User).filter(User.id == user_id).first()
    if user_id:
        return_dict = add_notifications(return_dict, session, user_id)
    else:
        return_dict['notifications'] = []
        return_dict['username'] = ""
    return_dict['api_base_url'] = API_URL
    return_dict['league_id'] = return_dict.get('league_id', DEFAULT_LEAGUE)
    return return_dict


def post_api_json(url, data, fe_api_key=None):
    print("in postapijson")
    try:
        req = urllib2.Request(url, data=json.dumps(data),
                              headers={'apiKey': fe_api_key, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


def format_time(time_):
    return datetime.datetime.fromtimestamp(time_).strftime('%Y-%m-%d %H:%M:%S')

#!/usr/bin/env python3
"""A basic Flask app setup with config object
force a particular locale
"""
from flask import Flask, render_template, request
from flask_babel import Babel, _, gettext
from typing import Union
import pytz

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}
"""mocked user database table"""


class Config():
    """Babel configuration class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
babel = Babel(app)


def get_user() -> Union[dict, None]:
    """Retrieve user dict based on user_id

    Args:
        user_id (int): id of requested user

    Returns:
        user dict if user_id exists, else None
    """
    try:
        user_id = request.args.get('login_as', None)
        return users[int(user_id)]
    except Exception:
        return None


@app.before_requests
def before_request():
    """find a user if any, and set it as a global on
    flask.g.user.

    Args:
        login_as (int)

    Returns:
        user and set as flask.g.user
    """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine best language match

    Return:
        language match
    """
    locale = request.args.get('locale', None)

    if locale and locale in app.config['LANGUAGES']:
        return locale

    locale = request.headers.get('locale', None)
    if locale and locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """Get  correct time zone"""
    timezone = request.args.get('timezone')
    if timezone:
        if timezone in pytz.all_timezones:
            return timezone
        else:
            raise pytz.exceptions.UnknownTimeZoneError
    try:
        user_id = request.args.get('login_as')
        user = users[int(user_id)]
        timezone = user['timezone']
    except Exception:
        timezone = None
    if timezone:
        if timezone in pytz.all_timezones:
            return timezone
        else:
            raise pytz.exceptions.UnknownTimeZoneError
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', methods=['GET'], strict_slashes=False)
def root():
    """
    Single route that simply outputs
    'Welcome to Holberton' - page title
    'Hello World' - header

    Return:
        template html
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run()

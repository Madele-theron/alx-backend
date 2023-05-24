#!/usr/bin/env python3
"""A basic Flask app setup with config object
force a particular locale
"""
from flask import Flask, render_template, request
from flask_babel import Babel, _, gettext
from typing import Union

# User table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config():
    """Babel configuration class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


def get_user() -> Union[dict, None]:
    """Retrieve user dict based on user_id

    Args:
        user_id (int): id of requested user

    Returns:
        user dict if user_id exists, else None
    """
    login_user = request.args.get('login_as', None)

    if login_user is None:
        return None

    user: dict = {}
    user[login_user] = users.get(int(login_user))

    return user[login_user]


@app.before_requests
def before_request(login_as: int = None):
    """find a user if any, and set it as a global on
    flask.g.user.

    Args:
        login_as (int)

    Returns:
        user and set as flask.g.user
    """
    user: dict = get_user()
    g.user = user
    print(user)


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


@app.route('/', methods=['GET'], strict_slashes=False)
def hello_world():
    """
    Single route that simply outputs
    'Welcome to Holberton' - page title
    'Hello World' - header

    Return:
        template html
    """
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

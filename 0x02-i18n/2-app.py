#!/usr/bin/env python3
"""A basic Flask app setup with config object"""
from flask import Flask, render_template, request
from flask_babel import Babel
app = Flask(__name__)


class Config():
    """Babel configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine best language match

    Return:
        language match
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/')
def hello_world():
    """
    Single route that simply outputs
    'Welcome to Holberton' - page title
    'Hello World' - header

    Return:
        template html
    """
    return render_template('2-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

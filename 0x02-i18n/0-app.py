#!/usr/bin/env python3
"""A basic Flask app setup"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    Single route that simply outputs
    'Welcome to Holberton' - page title
    'Hello World' - header

    Return:
        template html
    """
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

"""
This is the app.py boilerplate
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    """
    Test Route
    """
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)

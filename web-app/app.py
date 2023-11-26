"""
This is the app.py boilerplate
"""

from time import sleep
from base64 import b64decode
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    """main page (only page)"""
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    """login. POST with photo in body."""
    # take image from body

    bodystr = request.get_data(cache=False, as_text=True, parse_form_data=False)
    imgdata = bodystr.split(";")[1].split(",")[1]
    # use with PIL:
    with Image.open(BytesIO(b64decode(imgdata))) as im:
        print(im.size)
        # im.show()

    # @TODO send image to ML client
    sleep(2)

    # dummy return @TODO
    status = "ok"
    username = "TestUser123"
    sid = "132uygsfd76f12"
    content = "this is my private diary!!!\n~~~~\nI put all \
        my secrets here and they will be locked with my face."
    return {
        "status": status,
        "username": username,
        "sid": sid,
        "content": content,
    }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

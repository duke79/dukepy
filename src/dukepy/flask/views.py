from dukepy.flask import app


@app.route("/")
def hello():
    return "Hello World!"

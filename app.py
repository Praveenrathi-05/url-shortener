from flask import Flask, redirect, request
from database import get_match, create_short_link, log_click

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is my server!"

@app.route("/<code>")
def redirect_to_url(code):
    result = get_match(code)
    if result is None:
        return "Short link not found."
    link_id, url = result
    log_click(link_id)
    return redirect(url)

@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    url = data["url"]
    code = create_short_link(url)
    return {"short_code": code}

if __name__ == "__main__":
    app.run(debug=True)
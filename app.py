from flask import Flask, redirect, request
from database import get_match, create_short_link, log_click, get_top_links_by_clicks, delete_link

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

@app.route("/<code>", methods = ["DELETE"])
def delete(code):
    result = get_match(code)
    if result is None:
        return "Short link not found."
    link_id, _ = result
    delete_link(link_id)
    return "Link deleted successfully"

@app.route("/api/top")
def get_limit_top_links():
    limit = request.args.get("limit", "5")
    try:
        limit = int(limit)
    except ValueError:
        return "Limit Should be Number."
    results = get_top_links_by_clicks(limit)
    data = []
    for result in results:
        data.append({"url":result[0], "clicks": result[1]})
    return data

if __name__ == "__main__":
    app.run(debug=True)
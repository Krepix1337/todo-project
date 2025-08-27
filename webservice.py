from flask import Flask, request
from resources import Entry, EntryManager

app = Flask(__name__)
FOLDER = '/tmp/'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/entries")
def get_entries():
    manager = EntryManager(FOLDER)
    manager.load()
    result = [entry.json() for entry in manager.entries]
    return result

@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    data = request.get_json()
    for item in data:
        entry = Entry.entry_from_json(item)
        entry_manager.entries.append(entry)

    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)


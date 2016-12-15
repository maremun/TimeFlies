#   encoding: utf8
#   app.py

from flask import Flask, current_app, request

from .models import connect_database
from .settings import DB_URI
from .utils import handle_update


app = Flask(__name__)
app.database = connect_database(DB_URI)


@app.teardown_appcontext
def shutdown_database():
    app.database.rollback()
    app.dtabase.remove()


@app.route('/webhook/', methods=['POST'])
def index():
    update = request.json
    database = current_app.database
    handle_update(update, None, database)
    return '', 200

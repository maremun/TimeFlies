#   encoding: utf8
#   app.py

from flask import Flask, current_app, render_template, request

from .models import connect_database
from .settings import DB_URI
from .utils import handle_update


app = Flask(__name__)
app.database = connect_database(DB_URI)


@app.teardown_appcontext
def shutdown_database(error=None):
    app.database.rollback()
    app.database.remove()


@app.route('/webhook/', methods=['POST'])
def webhook():
    update = request.json
    database = current_app.database
    handle_update(update, None, database)
    return '', 200


@app.route('/admin/', methods=['GET'])
def index():
    num_users = current_app.database.execute("""
        SELECT
            COUNT(id) AS cnt
        FROM users;
        """).fetchone()['cnt']
    num_timelapses = current_app.database.execute("""
        SELECT
            COUNT(id) AS cnt
        FROM timelapse;
        """).fetchone()['cnt']

    return render_template('admin/index.html',
                           num_users=num_users,
                           num_timelapses=num_timelapses)


@app.route('/admin/users/', methods=['GET'])
def users():
    users = current_app.database.execute("""
        SELECT
            *
        FROM users;
        """).fetchall()
    return render_template('admin/users.html', users=users)


@app.route('/admin/timelapses/', methods=['GET'])
def timelapses():
    timelapses = current_app.database.execute("""
        SELECT
            t.id AS timelapse_id,
            t.user_id AS user_id,
            t.timelapse_name AS timelapse_name,
            u.username AS username
        FROM timelapse t
        JOIN users u ON u.id = t.user_id;
        """).fetchall()
    return render_template('admin/timelapses.html', timelapses=timelapses)

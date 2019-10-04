from flask import Flask
import sqlite3
import json

app = Flask(__name__)

def db_query(query):
    conn = sqlite3.connect(app.config['db'])
    c = conn.cursor()
    c.execute(query)
    res = c.fetchall()
    conn.close()

    return res

@app.route("/")
def hello():
    return "hello world"

@app.route("/tablas")
def obtenerTablas():
    res = db_query("select * from sqlite_master where type='table';")
    return json.dumps(res)

@app.route("/tablas/<name>")
def tabla(name):
    res = db_query("select * from {}".format(name))
    return json.dumps(res)

if __name__ == "__main__":
    app.config['db'] = "ejemplo.db"
    app.run()
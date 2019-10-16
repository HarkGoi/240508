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
def saludo():
    return "Explorer for {}".format(app.config['db'])


@app.route("/tablas")
def obtenertablas():
    res = db_query("select * from sqlite_master where type='table';")
    return json.dumps(res)


@app.route("/tablas/<name>")
def tabla(name):
    res = db_query("select * from {};".format(name))
    return json.dumps(res)

@app.route("/tablas/<name>/info")
def infotabla(name):
    conn = sqlite3.connect(app.config['db'])
    c = conn.cursor()
    c.execute("pragma table_info({});".format(name))
    lc = []
    res = c.fetchone()
    while res != None:
        lc.append(res[1])
        print (res[1])
        res = c.fetchone()
    c.execute("select count(*) from {}".format(name))
    l = []
    l.append(lc)
    l.append(c.fetchone())
    conn.close()
    return json.dumps(l)

if __name__ == "__main__":
    app.config['db'] ="ejemplo.db"
    app.run()
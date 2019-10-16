from flask import Flask, render_template
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

def comprobar_tabla(name):
    # comprobamos la existencia de la tabla
    conn = sqlite3.connect(app.config['db'])
    c = conn.cursor()
    c.execute("select * from sqlite_master where type='table';")
    res = c.fetchone()
    while res != None:
        if res[2] == name:
            conn.close()
            return True
        res = c.fetchone()
    conn.close()
    return False


@app.route("/")
def saludo():
    return "Explorer for {}".format(app.config['db'])


@app.route("/html/tablas")
def obtenertablas():
    res = db_query("select * from sqlite_master where type='table';")
    return render_template('infotablas.html', tablas=res)


@app.route("/html/tablas/<name>")
def tabla(name):
    if comprobar_tabla(name) == False:
        return render_template('error.html', name=name)
    # obtenemos los nombres de las columnas
    conn = sqlite3.connect(app.config['db'])
    c = conn.cursor()
    c.execute("pragma table_info({});".format(name))
    lc = []
    res = c.fetchone()
    while res != None:
        lc.append(res[1])
        res = c.fetchone()
    # y el contenido de la tabla
    res = db_query("select * from {};".format(name))
    return render_template('contenidotablas.html', listacolumnas=lc, name=name, tabla=res)

@app.route("/html/tablas/<name>/info")
def infotabla(name):
    if comprobar_tabla(name) == False:
        return render_template('error.html', name=name)
    # obtenemos los nombres de las columnas
    conn = sqlite3.connect(app.config['db'])
    c = conn.cursor()
    c.execute("pragma table_info({});".format(name))
    lc = []
    res = c.fetchone()
    while res != None:
        lc.append(res[1])
        res = c.fetchone()
    c.execute("select count(*) from {}".format(name))
    numregistros = c.fetchone()[0]
    conn.close()
    return render_template('infotabla.html', listacolumnas=lc, name=name, numregistros=numregistros, anchura=len(lc))


@app.route("/tablas")
def obtenertablasJ():
    res = db_query("select * from sqlite_master where type='table';")
    return json.dumps(res)


@app.route("/tablas/<name>")
def tablaJ(name):
    res = db_query("select * from {};".format(name))
    return json.dumps(res)

@app.route("/tablas/<name>/info")
def infotablaJ(name):
    conn = sqlite3.connect(app.config['db'])
    c = conn.cursor()
    c.execute("pragma table_info({});".format(name))
    lc = []
    res = c.fetchone()
    while res != None:
        lc.append(res[1])
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
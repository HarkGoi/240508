from flask import Flask, render_template
import sqlite3
import json
import sys

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
    while res is not None:
        if res[2] == name:
            conn.close()
            return True
        res = c.fetchone()
    conn.close()
    return False


def obtener_nombres_columnas(name):
    conn = sqlite3.connect(app.config['db'])
    c = conn.cursor()
    c.execute("pragma table_info({});".format(name))
    lc = []
    res = c.fetchone()
    while res is not None:
        lc.append(res[1])
        res = c.fetchone()
    conn.close()
    return lc

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
    lc = obtener_nombres_columnas(name)
    # y el contenido de la tabla
    res = db_query("select * from {};".format(name))
    return render_template('contenidotablas.html', listacolumnas=lc, name=name, tabla=res)


@app.route("/html/tablas/<name>/info")
def infotabla(name):
    if not comprobar_tabla(name):
        return render_template('error.html', name=name)
    # obtenemos los nombres de las columnas
    lc = obtener_nombres_columnas(name)
    # c.execute("select count(*) from {}".format(name))
    # numregistros = c.fetchone()[0]
    numregistros = db_query("select count(*) from {};".format(name))[0][0]
    return render_template('infotabla.html', listacolumnas=lc, name=name, numregistros=numregistros, anchura=len(lc))


@app.route("/tablas")
def obtenertablasj():
    res = db_query("select * from sqlite_master where type='table';")
    return json.dumps(res)


@app.route("/tablas/<name>")
def tablaj(name):
    res = db_query("select * from {};".format(name))
    return json.dumps(res)

@app.route("/tablas/<name>/info")
def infotablaj(name):
    conn = sqlite3.connect(app.config['db'])
    c = conn.cursor()
    c.execute("pragma table_info({});".format(name))
    lc = []
    res = c.fetchone()
    while res is not None:
        lc.append(res[1])
        res = c.fetchone()
    c.execute("select count(*) from {}".format(name))
    l = [lc, c.fetchone()]
    conn.close()
    return json.dumps(l)


if __name__ == "__main__":
    app.config['db'] = sys.argv[1]
    app.run()
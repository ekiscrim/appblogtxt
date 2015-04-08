# -*- coding: utf-8 -*-

from flask import Flask, render_template,request, g, flash,redirect,url_for
import os
from sqlite3 import dbapi2 as sqlite3

#ver: https://github.com/code-haven/FlaskBlog/blob/master/flaskblog.py

#la aplicacion
app = Flask(__name__)
app.config.from_object(__name__)
#cargar la configuracion por defecto
app.config.update(dict(
						DATABASE=os.path.join(app.root_path, 'post.db'),
						DEBUG=True,
						SECRET_KEY='probando',
						USERNAME='admin',
						PASSWORD='admin'
				))
app.config.from_envvar('POST_SETTINGS', silent=True)

def connect_db():
	'''Conecta con la base de datos especifica'''
	con = sqlite3.connect(app.config['DATABASE'])
	con.row_factory = sqlite3.Row
	return con
'''
La sentencia with se utiliza con objetos que soportan el protocolo 
de manejador de contexto y garantiza que una o varias sentencias 
serán ejecutadas automáticamente. Esto nos ahorra muchas líneas de código, 
a la vez que nos garantiza que ciertas operaciones serán realizadas sin que 
lo indiquemos explícitamente. Uno de los ejemplos más claros es cuando leemos 
un archivo de texto. Al terminar esta operación siempre es recomendable cerrar 
el archivo. Gracias a with esto ocurrirá automáticamente, 
sin necesidad de llamar al método close().
'''
def get_db():	
	'''abre una nueva conexion a la base de datos si esta aun no existe
	en el contexto actual
	'''
	if not hasattr(g,'post.db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
'''
@app.cli.command('initdb')
def initdb_command():
	"""Crear la tabla en la base de datos""" hacer desde linea de comandos
	init_db()
	print('Base de datos iniciada')
'''

@app.teardown_appcontext
def close_db(error):
	'''cierra la conexion de la db'''
	if hasattr(g,'post.db'):
		g.sqlite_db.close()

 # mostrar las entradas
@app.route('/')
def mostrar_post():
	db = get_db()
	cur = db.execute('SELECT title,author,textillo FROM post')
	entradas = cur.fetchall()
	return render_template('home.html',entradas=entradas)
# insertar una nueva entrada desde el fichero
@app.route('/', methods=['POST'])
def add_post():
	db = get_db()
	fichero = request.files['archivo']
	for linea in fichero.readlines():
		partir = linea.split('#')
		titulo = partir[1]
		autor = partir[2]
		texto = partir[3]
		db.execute('INSERT INTO post (title,author,textillo) VALUES (?,?,?)',[titulo,autor,texto])
		db.commit()
	flash('Entradas agregadas con exito')
	return redirect(url_for('mostrar_post'))
if __name__ == '__main__':
  app.run(debug=True)
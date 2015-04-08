# from flask_sqlalchemy import SQLAlchemy
# from routes import app
# db = SQLAlchemy(app)
# class Post(db.Model):
# 	__tablename__ ='post'
# 	id = db.Column(db.Integer,primary_key = True)
# 	title = db.Column(db.String(200), unique=True)
# 	author = db.Column(db.String(80))
# 	textito = db.Column(db.String(300))

# 	def __init__(self,titulo,autor,texto):
# 		self.title = titulo
# 		self.author = autor
# 		self.textito = texto
# 	def __repr__(self):
# 		return '<Titulo %r>' % self.textito
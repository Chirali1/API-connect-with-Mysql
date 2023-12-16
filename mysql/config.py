from flaskext.mysql import MySQL
from app import app

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Krishna@1234'
app.config['MYSQL_DATABASE_DB'] = 'student'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
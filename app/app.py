from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

from .config import Configuration
from .model_view import *

app: Flask = Flask(__name__)
app.config.from_object(Configuration)
db: SQLAlchemy = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from .model import *

# falk security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
# flask admin
admin = Admin(app, 'FlaskApp', url='/',
              index_view=HomeAdminView(name='Admin'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))

try:
    from distutils.debug import DEBUG
    from distutils.log import debug
    from flask import Flask
    from flask_cors import CORS
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy import MetaData, true
    from flask import render_template
    from flask_migrate import Migrate
except Exception as e:
    print (f"Failed to import required module: {e}")

from config import *
from utils import *

app = Flask(__name__)
app.config.update(app_config_dict)
CORS(app)


db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)


from services import setup 
from models.Role import Role as RoleModel
from models.Entity import Entity as EntityModel
from models.User import User as UserModel
from models.UserRoleMapping import UserRoleMapping as UserRoleMappingModel
from models.Country import Country
from models.UserSessions import UserSession
from models.analytics import analytics
from routes import User
from routes import weather
from routes import countries
from routes import analytics
from data.processJson import build_db_from_json

setup.add_roles_to_static_table()
setup.add_superadmin_to_users_table()

with app.app_context():
    db.create_all()
    build_db_from_json()
    

@app.route('/')
def ping():  # put application's code here
    return render_template('login.html') #not being used


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', DEBUG=True)

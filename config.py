import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data.sqlite')

app_config_dict = {
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}

secret_key = os.environ.get('secret_key', 'FT8H9ylGnZcfhCI5SX7Q2VL46IZd1vL1')
super_admin_password = os.environ.get('super_admin_password', 'ouC2gAbhsO')
api_key = os.environ.get('api_key', 'b306e87fcbf143d293a81212221304')
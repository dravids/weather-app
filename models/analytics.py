from app import db


class analytics(db.Model):
    """
    Analytics class
    Initializes table analytics for analytics api
    :param db.Model: Base class 
    :type db.Model: class
    """
    __tablename__ = 'analytics'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False)
    query = db.Column(db.String(255), nullable=False)



    def __init__(self, user_name, query):
        self.user_name = user_name
        self.query = query
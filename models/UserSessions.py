from app import db


class UserSession(db.Model):
    __tablename__ = 'usersession'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), default='active', nullable=False)
    inserted_at = db.Column(db.DateTime, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_name, token, status, inserted_at, expires_at, updated_at):
        self.user_name = user_name
        self.token = token
        self.status = status
        self.inserted_at = inserted_at
        self.expires_at = expires_at
        self.updated_at = updated_at


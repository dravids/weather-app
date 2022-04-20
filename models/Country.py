from app import db


class Country(db.Model):
    __tablename__ = 'Countries'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    country = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)



    def __init__(self, country, city):
        self.country = country
        self.city = city

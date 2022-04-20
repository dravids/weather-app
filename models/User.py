from app import db


class User(db.Model):
    __tablename__ = 'users'
    user_name = db.Column(db.String(255), primary_key=True, nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    roles = db.relationship('Role', secondary='user_roles_mapping')
    entities = db.relationship('Entity', secondary='user_entities_mapping')

    def __init__(self, user_name, user_email, password, first_name, last_name):
        self.user_name = user_name
        self.user_email = user_email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
    
    def __repr__(self):
        return f"User('{self.user_name}', '{self.user_email}', '{self.user_email}', '{self.user_email}')"



    @classmethod
    def return_all(cls):

        def to_json(obj):
            return {
                'Username': obj.user_name,
                'Email': obj.user_email
            }

        return {'users': [to_json(user) for user in cls.query.all()]}

    @classmethod
    def delete_all(cls):

        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()

            return {'message': f'{num_rows_deleted} row(s) deleted'}
        except Exception as e:

            return {'message': f'Exception occured: {e}'}

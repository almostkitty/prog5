from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    bonus_level = db.Column(db.String(50), default='Basic')
    
    def __repr__(self):
        return f"User('{self.username}')"

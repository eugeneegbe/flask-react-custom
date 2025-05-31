from service import db

class UserModel(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(80), unique=True, nullable=False)
    pre_langs = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"User(username= {self.username}, pref_langs= {self.pre_langs})"

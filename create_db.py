from service import app, db
from service.models import UserModel

with app.app_context():
    db.create_all()

from app.database import db

class Plan(db.Model):
    __tablename__ = "plan"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    date_generation = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

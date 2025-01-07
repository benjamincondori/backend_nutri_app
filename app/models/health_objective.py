from app.database import db

class HealthObjective(db.Model):
    __tablename__ = "health_objective"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    other_objetive = db.Column(db.String(255), nullable=True)
    update_date = db.Column(db.DateTime, nullable=False)
    number_days = db.Column(db.Integer, nullable=False)
    health_profile_id = db.Column(db.Integer, db.ForeignKey('health_profile.id'))
    #health_profile = db.relationship('HealthProfile', backref='health_objective')

    def __str__(self):
        return(
            f'id: {self.id}, '
            f'name: {self.name}, '
            f'description: {self.description}, '
            f'update_date: {self.update_date}'
        )
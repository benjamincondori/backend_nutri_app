from app.database import db

class PhysicalActivity(db.Model):
    __tablename__ = "physical_activity"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    PAL = db.Column(db.Float, nullable=False)
    health_profile = db.relationship('HealthProfile', back_populates='physical_activity', uselist=False, cascade="all, delete-orphan")

    def __str__(self):
        return(
            f'id: {self.id}, '
            f'name: {self.name}, '
            f'description: {self.description}, '
            f'PAL: {self.PAL}'
            )
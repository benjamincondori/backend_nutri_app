from app.database import db

class PlanMeal(db.Model):
    __tablename__ = "plan_meal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("plan.id"), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    
    # Relaciones con Plan y Meal
    plan = db.relationship("Plan", backref=db.backref('plan_meal', lazy='dynamic'))
    meal = db.relationship("Meal", backref=db.backref('plan_meal', lazy='dynamic'))

    def __str__(self):
        return (
            f'id: {self.id}, '
            f'plan_id: {self.plan_id}, '
            f'meal_id: {self.meal_id}, '
            f'day: {self.day}'
        )

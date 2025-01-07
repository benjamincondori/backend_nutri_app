from app.database import db

class MealFood(db.Model):
    __tablename__ = "meal_food"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey("food.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1.0)  # Porción o cantidad del alimento
    type_quantity =  db.Column(db.String(50), nullable=False)
    # Relaciones con Meal y Food
    #meal = db.relationship("Meal", backref=db.backref("meal_food_associations", cascade="all, delete-orphan"))
    #food = db.relationship("Food", backref=db.backref("meal_food_associations", cascade="all, delete-orphan"), single_parent=True)
    meal = db.relationship("Meal", backref=db.backref('meal_food', lazy='dynamic'))
    food = db.relationship("Food", backref=db.backref('meal_food', lazy='dynamic'))

    def __str__(self):
        return (
            f'id: {self.id}, '
            f'meal_id: {self.meal_id}, '
            f'food_id: {self.food_id}, '
            f'quantity: {self.quantity}'
        )

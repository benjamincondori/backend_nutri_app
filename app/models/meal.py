from app.database import db

class Meal(db.Model):
    __tablename__ = "meal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)
    total_calories = db.Column(db.Float, nullable=False)
    total_proteins = db.Column(db.Float, nullable=False)
    total_fats = db.Column(db.Float, nullable=False)
    total_carbohydrates = db.Column(db.Float, nullable=False)

    # Relación con la tabla intermedia MealFood
    #meal_food_associations = db.relationship("MealFood", backref="meal_association", cascade="all, delete-orphan")


    def __str__(self):
        return(
            f'id: {self.id}, '
            f'name: {self.name}, '
            f'status: {self.status}, '
            f'meal_type: {self.meal_type}, '
            f'total_calories: {self.total_calories}, '
            f'total_proteins: {self.total_proteins}, '
            f'total_fats: {self.total_fats}, '
            f'total_carbohydrates: {self.total_carbohydrates}, '
        )
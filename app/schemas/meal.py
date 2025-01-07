from app.extensions import ma
from app.models.meal import Meal

class MealSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Meal
        include_relationships = True
        load_instance = True  # Permite deserializar a un objeto PhysicalActivity


meal_schema =MealSchema()  # Para un solo objetivo de salud
meals_schema = MealSchema(many=True)  # Para una lista de objetivos de salud
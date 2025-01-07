from app.extensions import ma
from app.models.health_objective import HealthObjective

class HealthObjectiveSchema(ma.SQLAlchemySchema):
    class Meta:
        model = HealthObjective
        include_relationships = True
        load_instance = True  # Permite deserializar a un objeto HealthObjective
    
healt_objective_schema = HealthObjectiveSchema()  # Para un solo objetivo de salud
health_objectives_schema = HealthObjectiveSchema(many=True)  # Para una lista de objetivos de salud
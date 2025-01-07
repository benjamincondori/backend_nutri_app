from marshmallow import Schema, fields

from app.extensions import ma
from app.models.health_profile import HealthProfile

class HealthProfileSchema(Schema):
    id = fields.Integer(dump_only=True)
    age = fields.Integer(required=True)
    weight = fields.Float(required=True)
    height = fields.Float(required=True)
    physical_activity = fields.String(required=True)
    update_date = fields.DateTime(required=True)
    health_restrictions = fields.String(required=False)
    user_id = fields.Integer(dump_only=True)
    birthday = fields.Date(required=True)
    gender = fields.String(required=True)

#     class Meta:
#         model = HealthProfile
#         include_relationships = True
#         load_instance = True  # Permite deserializar a un objeto HealthObjective

# health_profile_schema = HealthProfileSchema()  # Para un solo perfil de salud
# health_profiles_schema = HealthProfileSchema(many=True)  # Para una lista de perfiles de salud

from marshmallow import Schema, fields

from app.extensions import ma
# from app.models.user import User
# from app.models.health_profile import HealthProfile
# from app.models.health_objective import HealthObjective
from app.schemas.health_profile import HealthProfileSchema



class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    lastname = fields.String(required=True)
    telephone = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    url_image = fields.String(required=True)
    health_profile = fields.Nested(HealthProfileSchema)

#     health_profile = ma.Nested(HealthProfileSchema)  # Incluir datos del perfil de salud

#     class Meta:
#         model = User
#         include_relationships = True
#         load_instance = True

#     # Sobrescribiendo un campo para personalizarlo
#     password = ma.auto_field(load_only=True)  # Solo se puede deserializar

# # Instancias de esquemas
# user_schema = UserSchema()  # Para un solo usuario
# users_schema = UserSchema(many=True)  # Para una lista de usuarios

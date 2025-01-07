from app.extensions import ma
from app.models.physical_activity import PhysicalActivity

class PhysicalActivitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = PhysicalActivity
        include_relationships = True
        load_instance = True  # Permite deserializar a un objeto PhysicalActivity

    health_profile = ma.Nested('HealthProfileSchema', exclude=('physical_activity',))

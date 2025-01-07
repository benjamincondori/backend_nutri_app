from app.database import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    url_image = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), nullable=False, default='user')  # user o nutritionist
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    # health_profile = db.relationship('HealthProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    health_profile = db.relationship('HealthProfile', back_populates='user', uselist=False,
                                     cascade="all, delete-orphan")
    plans = db.relationship('Plan', backref='plan')

    def __repr__(self):
        return (
            f'User(id={self.id}, '
            f'name={self.name}, '
            f'lastname={self.lastname}, '
            f'telephone={self.telephone}, '
            f'email={self.email}, '
            f'url_image={self.url_image}), '
            f'type={self.type})'
        )


class Nutritionist(User):
    __tablename__ = "nutritionist"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # Campos adicionales específicos del nutricionista
    specialty = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'nutritionist',
    }

    def __repr__(self):
        return (
            f'Nutritionist(id={self.id}, '
            f'name={self.name}, '
            f'lastname={self.lastname}, '
            f'specialty={self.specialty}, '
        )

# https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg
# solidity (blockchain)

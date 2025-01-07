import os
from flask import Flask, request
import pandas as pd
import psycopg2
from datetime import datetime

from app.database import db
from app.models.meal import Meal
from app.models.physical_activity import PhysicalActivity
from app.models.user import User, Nutritionist
from app.models.health_profile import HealthProfile
from app.models.food import Food
from app.models.meal_food import MealFood
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import exists
from werkzeug.security import generate_password_hash


#función para cargar datos de tipos de actividad fisica predefinidas en la base de datos
def seed_data():
    # Datos predefinidos para PhysicalActivity
    activities = [
        {"name": "Sedentario", "description": "Poco o ningún ejercicio", "PAL": 1.2},
        {"name": "Ligeramente Activo", "description": "Ejercicio/deporte ligero 1-3 días a la semana", "PAL": 1.375},
        {"name": "Moderadamente Activo", "description": "Ejercicio/deporte moderado 3-5 días a la semana", "PAL": 1.55},
        {"name": "Muy Activo", "description": "Ejercicio/deporte intenso 6-7 días a la semana", "PAL": 1.725},
        {"name": "Extra Activo", "description": "Ejercicio muy intenso o trabajo físico", "PAL": 1.9}
    ]

    # Verificar e insertar solo si la actividad no existe
    for activity_data in activities:
        # Comprobar si ya existe una actividad con el mismo nombre
        existing_activity = PhysicalActivity.query.filter_by(name=activity_data['name']).first()
        
        # Si no existe, crear una nueva actividad
        if not existing_activity:
            activity = PhysicalActivity(
                name=activity_data['name'],
                description=activity_data['description'],
                PAL=activity_data['PAL']
            )
            db.session.add(activity)

    # Commit para guardar las actividades en la base de datos
    db.session.commit()

    print("Datos de actividad física predefinidos cargados exitosamente.")

#función para cargar datos de usuarios y perfiles de salud predefinidos en la base de datos
def seed_users_health_profile():
    # Datos predefinidos para User
    users = [
        {
            "name": "Juan",
            "lastname": "Pérez",
            "telephone": "555-1234",
            "email": "juan.perez@example.com",
            "password": "securepassword123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 30,
                "weight": 75.5,
                "height": 1.78,
                "physical_activity_id": 3,  # Moderadamente Activo
                "health_restrictions": "Ninguna",
                "birthday": datetime(1994, 5, 15),
                "gender": "Masculino",
            },
        },
        {
            "name": "María",
            "lastname": "López",
            "telephone": "555-5678",
            "email": "maria.lopez@example.com",
            "password": "mypassword123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 25,
                "weight": 62.0,
                "height": 1.65,
                "physical_activity_id": 2,  # Ligeramente Activo
                "health_restrictions": "Diabetes",
                "birthday": datetime(1999, 7, 20),
                "gender": "Femenino",
            },
        },
        {
            "name": "Carlos",
            "lastname": "Gómez",
            "telephone": "555-8765",
            "email": "carlos.gomez@example.com",
            "password": "password123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 40,
                "weight": 85.0,
                "height": 1.75,
                "physical_activity_id": 1,  # Sedentario
                "health_restrictions": "Hipertensión",
                "birthday": datetime(1984, 3, 12),
                "gender": "Masculino",
            },
        },
        {
            "name": "Ana",
            "lastname": "Torres",
            "telephone": "555-2468",
            "email": "ana.torres@example.com",
            "password": "anasecret123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 50,
                "weight": 90.0,
                "height": 1.70,
                "physical_activity_id": 1,  # Sedentario
                "health_restrictions": "Problemas articulares",
                "birthday": datetime(1974, 1, 5),
                "gender": "Femenino",
            },
        },
        {
            "name": "Luis",
            "lastname": "Ramírez",
            "telephone": "555-1357",
            "email": "luis.ramirez@example.com",
            "password": "luispass123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 35,
                "weight": 78.0,
                "height": 1.80,
                "physical_activity_id": 4,  # Muy Activo
                "health_restrictions": "Ninguna",
                "birthday": datetime(1989, 9, 10),
                "gender": "Masculino",
            },
        },
        {
            "name": "Carmen",
            "lastname": "Martínez",
            "telephone": "555-3579",
            "email": "carmen.martinez@example.com",
            "password": "carmenpass123",
            "url_image": "http://example.com/image6.jpg",
            "health_profile": {
                "age": 60,
                "weight": 70.0,
                "height": 1.60,
                "physical_activity_id": 2,  # Ligeramente Activo
                "health_restrictions": "Enfermedad cardíaca",
                "birthday": datetime(1964, 2, 22),
                "gender": "Femenino",
            },
        },
        {
            "name": "Eduardo",
            "lastname": "Fernández",
            "telephone": "555-6543",
            "email": "eduardo.fernandez@example.com",
            "password": "edupass123",
            "url_image": "http://example.com/image7.jpg",
            "health_profile": {
                "age": 45,
                "weight": 95.0,
                "height": 1.85,
                "physical_activity_id": 3,  # Moderadamente Activo
                "health_restrictions": "Sobrepeso",
                "birthday": datetime(1979, 12, 3),
                "gender": "Masculino",
            },
        },
        {
            "name": "Gloria",
            "lastname": "Sánchez",
            "telephone": "555-7412",
            "email": "gloria.sanchez@example.com",
            "password": "gloriaspass123",
            "url_image": "http://example.com/image8.jpg",
            "health_profile": {
                "age": 28,
                "weight": 55.0,
                "height": 1.62,
                "physical_activity_id": 4,  # Muy Activo
                "health_restrictions": "Bajo peso",
                "birthday": datetime(1996, 6, 18),
                "gender": "Femenino",
            },
        },
        {
            "name": "Ricardo",
            "lastname": "Vargas",
            "telephone": "555-8523",
            "email": "ricardo.vargas@example.com",
            "password": "ricardopass123",
            "url_image": "http://example.com/image9.jpg",
            "health_profile": {
                "age": 20,
                "weight": 70.0,
                "height": 1.75,
                "physical_activity_id": 5,  # Extra Activo
                "health_restrictions": "Ninguna",
                "birthday": datetime(2004, 11, 25),
                "gender": "Masculino",
            },
        },
        {
            "name": "Elena",
            "lastname": "Morales",
            "telephone": "555-9638",
            "email": "elena.morales@example.com",
            "password": "elenapass123",
            "url_image": "http://example.com/image10.jpg",
            "health_profile": {
                "age": 18,
                "weight": 50.0,
                "height": 1.55,
                "physical_activity_id": 3,  # Moderadamente Activo
                "health_restrictions": "Trastornos alimenticios",
                "birthday": datetime(2006, 4, 15),
                "gender": "Femenino",
            },
        },
    ]
     
    for user_data in users:
        # Encriptar la contraseña antes de crear el usuario
        hashed_password = generate_password_hash(user_data["password"])

        # Crear usuario
        user = User(
            name=user_data["name"],
            lastname=user_data["lastname"],
            telephone=user_data["telephone"],
            email=user_data["email"],
            password=hashed_password,
            url_image=user_data["url_image"],
        )
        db.session.add(user)
        db.session.commit()  # Guardar para obtener el ID del usuario

        # Crear perfil de salud
        health_profile_data = user_data["health_profile"]
        health_profile = HealthProfile(
            age=health_profile_data["age"],
            weight=health_profile_data["weight"],
            height=health_profile_data["height"],
            update_date=datetime.utcnow(),
            health_restrictions=health_profile_data["health_restrictions"],
            birthday=health_profile_data["birthday"],
            gender=health_profile_data["gender"],
            user_id=user.id,
            physical_activity_id=health_profile_data["physical_activity_id"],
        )
        db.session.add(health_profile)

        # Guardar todos los cambios
        db.session.commit()

        print("Usuarios y perfiles de salud cargados exitosamente.")

    # Crear un nutricionista
    nutritionist = Nutritionist(
        name="Marcos",
        lastname="Lopez",
        telephone="555-1122",
        email="marcos@gmail.com",
        password=generate_password_hash("123456"),  # Asegúrate de hashear la contraseña
        url_image="https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
        specialty="Nutrición Clínica"
    )

    # Agregar a la base de datos
    db.session.add(nutritionist)
    db.session.commit()

    print(f"Nutricionista creado exitosamente.")


#funcion para dar formato comidas
def load_meal (comidas):
    array_comidas = []
    # Inserción de comidas y sus alimentos en el arreglo
    for comida in comidas:
        nombre_comida = comida[0]  # Nombre de la comida
        tipo_comida = comida[1]  # Tipo de la comida (desayuno, almuerzo, cena)
        alimentos = comida[2]  # Alimentos de la comida
        
        # Arreglo para los alimentos de esta comida
        alimentos_comida = []

        # Para cada alimento en la comida
        for alimento in alimentos:
            alimento_comida = {
                "nombre": alimento["alimento"],  # Nombre del alimento
                "cantidad_alimento": alimento["cantidad"],  # Cantidad del alimento
                "tipo_alimento": alimento["tipo"]  # Tipo del alimento (gramos o porción)
            }
            alimentos_comida.append(alimento_comida)  # Agregar el alimento al arreglo de alimentos

        # Guardar la comida junto con sus alimentos
        comida_completa = {
            "nombre_comida": nombre_comida,
            "tipo_comida": tipo_comida,
            "alimentos": alimentos_comida
        }
        array_comidas.append(comida_completa)  # Agregar la comida completa al arreglo final
    
    return array_comidas  #

#funcion para cargar la columna "measure" en la tabla Food
# Seeder function
def seed_food_measures():
    foods_to_update = {
        'Bistec de ternera': 'gramo',
        'Buey semi graso': 'gramo',
        'Cabrito': 'gramo',
        'Cerdo carne magra': 'gramo',
        'Cerdo carne grasa': 'gramo',
        'Ciervo': 'gramo',
        'Codorniz': 'gramo',
        'Conejo': 'gramo',
        'Cordero Lechal': 'gramo',
        'Cordero (Pierna)': 'gramo',
        'Faisán': 'gramo',
        'Hígado de cerdo': 'gramo',
        'Higado de vacuno': 'gramo',
        'Jabalí': 'gramo',
        'Lacón': 'gramo',
        'Liebre': 'gramo',
        'Pato': 'gramo',
        'Pavo pechuga': 'gramo',
        'Pavo muslo': 'gramo',
        'Perdiz': 'gramo',
        'Pollo muslo': 'gramo',
        'Pollo pechuga': 'gramo',
        'Almeja': 'gramo',
        'Anguila': 'gramo',
        'Arenque': 'gramo',
        'Atún fresco': 'gramo',
        'Bacalao': 'gramo',
        'Boquerón': 'gramo',
        'Caballa': 'gramo',
        'Calamar': 'gramo',
        'Dorada': 'gramo',
        'Gallo': 'gramo',
        'Gamba': 'gramo',
        'Langosta': 'gramo',
        'Lenguado': 'gramo',
        'Lubina': 'gramo',
        'Lucio': 'gramo',
        'Mejillones': 'gramo',
        'Merluza': 'gramo',
        'Mero': 'gramo',
        'Pez espada': 'gramo',
        'Pulpo': 'gramo',
        'Rodaballo': 'gramo',
        'Salmón': 'gramo',
        'Salmonete': 'gramo',
        'Sardina': 'gramo',
        'Sepia': 'gramo',
        'Trucha': 'gramo',
        'Huevo entero (100 gr)': 'unidad',
        'Huevo entero pequeño (50 gr)': 'unidad',
        'Yema (17 gr)': 'gramo',
        'Clara (33 gr)': 'gramo',
        'Aguacate': 'unidad',
        'Albaricoque': 'unidad',
        'Arándano': 'gramo',
        'Cereza': 'unidad',
        'Ciruela': 'unidad',
        'Frambuesa': 'gramo',
        'Fresa': 'gramo',
        'Granada': 'unidad',
        'Grosella': 'gramo',
        'Higo fresco': 'unidad',
        'Limón': 'unidad',
        'Mandarina': 'unidad',
        'Mango': 'unidad',
        'Manzana': 'unidad',
        'Melocotón': 'unidad',
        'Melón': 'unidad',
        'Mora': 'gramo',
        'Naranja': 'unidad',
        'Arandano':'unidad',
        'Níspero': 'unidad',
        'Polenta (Harina de Maíz)': 'gramo',
        'Piña': 'unidad',
        'Pera': 'unidad',
        'Plátano': 'unidad',
        'Pomelo': 'unidad',
        'Sandía': 'unidad',
        'Uva': 'gramo',
        'Almendra': 'gramo',
        'Avellana': 'gramo',
        'Cacahuete': 'gramo',
        'Castaña': 'gramo',
        'Ciruela pasa': 'gramo',
        'Dátil seco': 'gramo',
        'Higo seco': 'gramo',
        'Nuez': 'gramo',
        'Piñón': 'gramo',
        'Pistacho': 'gramo',
        'Uva Pasa': 'gramo',
        'Ajo': 'unidad',
        'Alcachofa': 'unidad',
        'Apio': 'gramo',
        'Berenjena': 'gramo',
        'Berro': 'gramo',
        'Brécol': 'gramo',
        'Calabacín': 'gramo',
        'Calabaza': 'gramo',
        'Cardo': 'gramo',
        'Cebolla': 'gramo',
        'Col lombarda': 'gramo',
        'Coles de Bruselas': 'gramo',
        'Coliflor': 'gramo',
        'Espárrago': 'gramo',
        'Espinaca': 'gramo',
        'Guisantes frescos': 'gramo',
        'Haba fresca': 'gramo',
        'Hinojo': 'gramo',
        'Lechuga': 'gramo',
        'Nabo': 'gramo',
        'Patata': 'unidad',
        'Pepino': 'unidad',
        'Puerro': 'gramo',
        'Remolacha': 'unidad',
        'Repollo': 'gramo',
        'Seta': 'gramo',
        'Tomate': 'unidad',
        'Trufa': 'gramo',
        'Zanahoria': 'gramo',
        'Alubia (judía seca)': 'gramo',
        'Garbanzo': 'gramo',
        'Guisantes secos': 'gramo',
        'Haba seca': 'gramo',
        'Lenteja': 'gramo',
        'Arroz': 'gramo',
        'Cebada': 'gramo',
        'Centeno': 'gramo',
        'Copos de Maiz': 'gramo',
        'Harina Integral': 'gramo',
        'Galleta tipo María': 'unidad',
        'Harina': 'gramo',
        'Maíz': 'gramo',
        'Pan Blanco': 'rebanada',
        'Pan Integral': 'rebanada',
        'Pan Tostado': 'rebanada',
        'Pasta al huevo': 'gramo',
        'Pasta de sémola': 'gramo',
        'Polenta (Harina de Maíz)': 'gramo',
        'Sémola': 'gramo',
        'Tapioca': 'gramo',
        'Trigo duro': 'gramo',
        'Aceite de oliva': 'mililitro',
        'Aceite de semillas': 'mililitro',
        'Mantequilla': 'gramo',
        'Manteca de cerdo': 'gramo',
        'Margarina': 'gramo',
        'Leche entera': 'mililitro',
        'Leche semidesnatada': 'mililitro',
        'Leche desnatada': 'mililitro',
        'Yogur entero': 'unidad',
        'Yogur desnatado': 'unidad',
        'Yogur con frutas': 'unidad',
        'Nata': 'mililitro',
        'Brie': 'gramo',
        'Camembert': 'gramo',
        'Cheddar': 'gramo',
        'Edam': 'gramo',
        'Emmental': 'gramo',
        'Gruyère': 'gramo',
        'Mozzarella': 'gramo',
        'Parmesano': 'gramo',
        'Queso de Oveja': 'gramo',
        'Requesón': 'gramo',
        'Roquefort': 'gramo',
        'Chocolate': 'gramo',
        'Miel': 'gramo',
    }

    for food_name, measure in foods_to_update.items():
        food = Food.query.filter_by(name=food_name).first() 
        if food:
            print(f"Antes de la actualización: {food.name}, {food.measure}")
            food.measure = measure
            print(f"Después de la actualización: {food.name}, {food.measure}")
        else:
            print("no existe food")    
    db.session.commit()

    print("Food measures updated successfully.")

#función para cargar datos de alimentos predefinidos en la base de datos
def seed_food():
    base_dir = os.getcwd()  # Directorio base (raíz del proyecto)
    filepath = os.path.join(base_dir, 'templates', 'alimentos.xlsx')
    quantity = 0  # Contador de alimentos insertados

    # Verificar si el archivo existe
    if not os.path.exists(filepath):
        print(f"El archivo {filepath} no existe.")
        return

    try:
        # Leer el archivo Excel
        df = pd.read_excel(filepath)

        # Verificar que las columnas necesarias existan
        required_columns = ['nombre', 'descripcion', 'calorias', 'proteinas', 
                            'grasas', 'carbohidratos', 'imagen_url', 'categoria', 'beneficios']
        if not all(col in df.columns for col in required_columns):
            print(f"El archivo Excel no contiene las columnas necesarias: {required_columns}")
            return
        
                # Limpiar datos en el DataFrame
        df = df.fillna('')  # Reemplazar NaN con cadenas vacías
        df['nombre'] = df['nombre'].str.strip()  # Eliminar espacios en blanco al inicio y al final
        df['descripcion'] = df['descripcion'].str.strip()
        df['imagen_url'] = df['imagen_url'].str.strip()
        df['categoria'] = df['categoria'].str.strip()
        df['beneficios'] = df['beneficios'].str.strip()

        # Insertar datos en la tabla
        for index, row in df.iterrows():
            try:
                # Reemplazar las comas por puntos y convertir a float, ignorando valores nulos
                calories = float(str(row['calorias']).replace(',', '.')) if pd.notnull(row['calorias']) and row['calorias'] != 0 else None
                proteins = float(str(row['proteinas']).replace(',', '.')) if pd.notnull(row['proteinas']) and row['proteinas'] != 0 else None
                fats = float(str(row['grasas']).replace(',', '.')) if pd.notnull(row['grasas']) and row['grasas'] != 0 else None
                carbohydrates = float(str(row['carbohidratos']).replace(',', '.')) if pd.notnull(row['carbohidratos']) and row['carbohidratos'] != 0 else None
                
                # Crear el objeto Food
                food = Food(
                    name=row['nombre'],
                    description=row['descripcion'],
                    calories=calories if calories is not None else 0.0,  # Si es None, asignamos 0.0
                    proteins=proteins if proteins is not None else 0.0,  # Lo mismo para proteínas
                    fats=fats if fats is not None else 0.0,              # Y grasas
                    carbohydrates=carbohydrates if carbohydrates is not None else 0.0,  # Y carbohidratos
                    image_url=row['imagen_url'],
                    category=row['categoria'],
                    benefits=row['beneficios']
                )
                db.session.add(food)
                quantity += 1
            except Exception as e:
                print(f"Error al procesar fila {index}: {e}")

        # Guardar todos los cambios en la base de datos
        db.session.commit()
        print(f"Se han cargado {quantity} alimentos.")
    except Exception as e:
        print(f"Error al leer o insertar datos: {e}")

def food_exists(name_food):
    try:
        exists_query = db.session.query(exists().where(Food.name == name_food)).scalar()
        
        if exists_query:
            print(f"Food with name {name_food} exists.")
        else:
            print(f"Food with name {name_food} does not exist.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_food(name_food):
    print(name_food)
    try:
            
        name_food = name_food.strip()
        exists_query = db.session.query(exists().where(Food.name == name_food)).scalar()

        if  exists_query:
            print(f" existe")
        else :
            print(f"no existe")


        all_foods = db.session.query(Food).all()
        #for food in all_foods:
            #print(f"Food in DB: {food.name}")
    
        comida = db.session.query(Food).filter(Food.name.ilike(name_food)).one_or_none()

        if comida is None:
            # Aquí puedes manejar el caso cuando no se encuentra la comida
            raise ValueError(f"alimento con nombre {name_food} no encontrado.")
        
        return comida
    
    except NoResultFound:
        # Aquí gestionamos el caso donde no se encuentra el alimento (aunque with `one_or_none()`, NoResultFound es menos probable)
        raise ValueError(f"Food with name {name_food} not found.")
    
    except Exception as e:
        # Manejar otros posibles errores
        print(f"An error occurred: {str(e)}")
        return None

def seed_meal():
    insert_meals(COMIDA1)
    insert_meals(COMIDA2)

    
def insert_meals(comidas):
    comidas = load_meal(comidas)  # Preparar los datos de las comidas y alimentos

    for comida in comidas:
        nombre_comida = comida["nombre_comida"]
        tipo_comida = comida["tipo_comida"]
        alimentos = comida["alimentos"]

        total_calories = 0
        total_proteins = 0
        total_fats = 0
        total_carbohydrates = 0

        # Crear la comida (Meal)
        meal = Meal(
            name=nombre_comida,
            meal_type=tipo_comida,
            status=False,
            total_calories=total_calories,
            total_proteins=total_proteins,
            total_fats=total_fats,
            total_carbohydrates=total_carbohydrates
        )
        
        # Añadir la comida a la base de datos
        db.session.add(meal)
        db.session.flush()  # Para obtener el ID de la comida recién insertada

        # Relacionar los alimentos con la comida
        for alimento in alimentos:
            # Obtener el alimento desde la base de datos
            food = get_food(alimento["nombre"])

            # Calcular las propiedades nutricionales según la cantidad
            cantidad = alimento["cantidad_alimento"]
            tipo = alimento["tipo_alimento"]

            # Realizamos la multiplicación de las propiedades nutricionales
            total_calories += food.calories * (cantidad / 100) if food.calories else 0
            total_proteins += food.proteins * (cantidad / 100) if food.proteins else 0
            total_fats += food.fats * (cantidad / 100) if food.fats else 0
            total_carbohydrates += food.carbohydrates * (cantidad / 100) if food.carbohydrates else 0

            # Insertar la relación de la comida con el alimento
            meal_food = MealFood(
                meal_id=meal.id,
                food_id=food.id,
                quantity=cantidad,
                type_quantity=tipo
            )
            db.session.add(meal_food)
            print(f"Se han cargado comidas.")


        # Actualizar las propiedades nutricionales totales de la comida
        meal.total_calories = total_calories
        meal.total_proteins = total_proteins
        meal.total_fats = total_fats
        meal.total_carbohydrates = total_carbohydrates

        db.session.commit()  # Guardar todo en la base de datos


COMIDA1 = [
    # Desayuno
    [  
        "Desayuno Energético",
        "desayuno",
        [
            {"alimento": "Huevo entero (100 gr)", "cantidad": 2, "tipo": "porción"},  # Porciones
            {"alimento": "Aguacate", "cantidad": 1, "tipo": "porción"},  # Porciones
            {"alimento": "Pan Integral", "cantidad": 2, "tipo": "porción"}  # Porciones
        ]
    ],
    
    # Almuerzo
    [
        "Almuerzo Alto en Proteínas",
        "almuerzo",
        [
            {"alimento": "Pavo pechuga", "cantidad": 150, "tipo": "gramos"},  # Gramos
            {"alimento": "Espárrago", "cantidad": 100, "tipo": "gramos"},  # Gramos
            {"alimento": "Arroz", "cantidad": 80, "tipo": "gramos"}  # Gramos
        ]
    ],
    
    # Cena
    [
        "Cena Ligera",
        "cena",
        [
            {"alimento": "Pollo pechuga", "cantidad": 120, "tipo": "gramos"},  # Gramos
            {"alimento": "Lechuga", "cantidad": 50, "tipo": "gramos"},  # Gramos
            {"alimento": "Tomate", "cantidad": 50, "tipo": "gramos"}  # Gramos
        ]
    ]
]



COMIDA2 = [
    # Día 1

    # Desayuno
    ["Leche con claras de huevo y frutas", 
     "desayuno",
        [
            {"alimento": "Leche entera", "cantidad": 50, "tipo": "gramos"},
            {"alimento": "Fresa", "cantidad": 50, "tipo": "gramos"},
            {"alimento": "Almendra", "cantidad": 15, "tipo": "gramos"}
        ]
    ],

    # Almuerzo
    ["Pollo con arroz integral y brócoli", 
    "almuerzo",
        [
            {"alimento": "Pollo pechuga", "cantidad": 200, "tipo": "gramos"},
            {"alimento": "Arroz", "cantidad": 100, "tipo": "gramos"},
            {"alimento": "Brécol", "cantidad": 100, "tipo": "gramos"},
            {"alimento": "Aceite de oliva", "cantidad": 1, "tipo": "porcion"}
        ]
    ],

    # Cena
    ["Pescado (salmón) con patata y espárragos",
    "cena",
 
        [
            {"alimento": "Salmón", "cantidad": 200, "tipo": "gramos"},
            {"alimento": "Patata", "cantidad": 150, "tipo": "gramos"},
            {"alimento": "Espárrago", "cantidad": 100, "tipo": "gramos"},
            {"alimento": "Aceite de oliva", "cantidad": 1, "tipo": "porcion"}
        ]
    ],

    # Día 2

    # Desayuno
    ["Yogur con granola, frutos rojos y nueces",
    "desayuno",
        [
            {"alimento": "Yogur entero", "cantidad": 200, "tipo": "gramos"},
            {"alimento": "Nuez", "cantidad": 15, "tipo": "gramos"}
        ]
    ],

    # Almuerzo
    ["Carne magra de cerdo y zanahorias", 
     "almuerzo",
        [
            {"alimento": "Cerdo carne magra", "cantidad": 200, "tipo": "gramos"},
            {"alimento": "Zanahoria", "cantidad": 100, "tipo": "gramos"},
            {"alimento": "Aceite de oliva", "cantidad": 1, "tipo": "porcion"}
        ]
    ],

    # Cena
    ["Pechuga de pavo con puré de calabaza",
    "cena",
        [
            {"alimento": "Pavo pechuga", "cantidad": 200, "tipo": "gramos"},
            {"alimento": "Calabaza", "cantidad": 150, "tipo": "gramos"},
            {"alimento": "Espinaca", "cantidad": 100, "tipo": "gramos"},
            {"alimento": "Aceite de oliva", "cantidad": 1, "tipo": "porcion"}
        ]
    ],

    # Día 3

    # Desayuno
    ["Tostadas de pan integral con aguacate y huevo", 
     "desayuno",
        [
            {"alimento": "Pan Integral", "cantidad": 2, "tipo": "porcion"},
            {"alimento": "Aguacate", "cantidad": 50, "tipo": "gramos"},
            {"alimento": "Huevo entero (100 gr)", "cantidad": 100, "tipo": "gramos"}
        ]
    ],

    # Almuerzo
    ["Pavo muslo y tomate", 
     "almuerzo",
        [
            {"alimento": "Pavo muslo", "cantidad": 200, "tipo": "gramos"},
            {"alimento": "Tomate", "cantidad": 100, "tipo": "gramos"},
            {"alimento": "Aceite de oliva", "cantidad": 1, "tipo": "porcion"}
        ]
    ],

    # Cena
    ["Merluza con arroz integral y guisantes", 
     "cena",
        [
            {"alimento": "Merluza", "cantidad": 200, "tipo": "gramos"},
            {"alimento": "Arroz", "cantidad": 100, "tipo": "gramos"},
            {"alimento": "Guisantes frescos", "cantidad": 100, "tipo": "gramos"},
            {"alimento": "Aceite de oliva", "cantidad": 1, "tipo": "porcion"}
        ]
    ]
]
import pandas as pd
import sys
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score

# Ajusta la ruta según sea necesario
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import create_app
from app.models.food import Food

# Crear la aplicación Flask
app = create_app()

# Diccionario que asigna el "Momento" según la categoría del alimento
category_to_momento = {
    "legumbres": ["almuerzo", "cena"],
    "otros": ["desayuno", "almuerzo", "cena"],
    "grasas": ["desayuno", "almuerzo", "cena"],
    "huevos": ["desayuno", "almuerzo", "cena"],
    "quesos": ["desayuno", "almuerzo", "cena"],
    "pescados": ["almuerzo", "cena"],
    "lacteos": ["desayuno", "cena"],
    "verduras/hortalizas": ["almuerzo", "cena"],
    "carnes": ["almuerzo", "cena"],
    "frutas": ["desayuno", "almuerzo", "cena"],
    "cereales y derivados": ["desayuno", "almuerzo", "cena"],
    "frutos secos": ["desayuno"]
}

with app.app_context():
 # Evento para detener el hilo de progreso

    # 1. Cargar los alimentos de la base de datos
    print("Cargando alimentos desde la base de datos")
    data_foods = Food.query.all()

    if not data_foods:
        print("\nNo hay alimentos en la base de datos. Se detiene el proceso.")
        exit()

    print(f"{len(data_foods)} alimentos cargados correctamente.")

    # Convertir a DataFrame
    print("Convirtiendo datos a DataFrame")
    df_food = pd.DataFrame([food.to_dict() for food in data_foods])

    # 2. Validar columnas necesarias
    print("Validando columnas necesarias")
    required_columns = ["name", "category", "calories", "proteins", "fats", "carbohydrates","measure"]
    for col in required_columns:
        if col not in df_food.columns:
            raise ValueError(f"Falta la columna requerida: {col}")
    print("Todas las columnas necesarias están presentes.")

    # 3. Crear etiquetas para "Momento"

    print("Creando etiquetas para 'Momento'")
    def assign_momento(category):
        return category_to_momento.get(category.lower(), ["desconocido"])
    df_food["Momento"] = df_food["category"].apply(assign_momento)

    # Expandir los momentos a columnas binarias
    for momento in ["desayuno", "almuerzo", "cena", "desconocido"]:
        df_food[momento] = df_food["Momento"].apply(lambda x: 1 if momento in x else 0)

    # Verificar distribución
    print("\nDistribución de los momentos:")
    print(df_food["Momento"].value_counts())
    # Continuar con los demás pasos...
    print("Preparando los datos para el modelo")
    le_category = LabelEncoder()

   #df_food["Momento"] = df_food["Momento"].apply(lambda x: x[0])
    df_food["Momento"] = df_food["Momento"].apply(
        lambda x: "/".join(x) if isinstance(x, list) else x
    )
    le_momento = LabelEncoder()
    df_food["Momento"] = le_momento.fit_transform(df_food["Momento"])
    le_momento.fit(["desayuno", "almuerzo", "cena", "almuerzo/cena", "desayuno/almuerzo/cena", "desayuno/cena"])
    df_food["category"] = le_category.fit_transform(df_food["category"])

    # Escalado de características
    print("Escalando características")
    scaler = StandardScaler()
    X = df_food[["calories", "proteins", "fats", "carbohydrates"]]
    X_scaled = scaler.fit_transform(X)

    # Dividir datos en entrenamiento y prueba
    print("Dividiendo datos en entrenamiento y prueba")
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, df_food["Momento"], test_size=0.2, random_state=42)

    # Entrenar el modelo
    print("Entrenando el modelo de Random Forest")
    modelo_momento = RandomForestClassifier(random_state=42)
    modelo_momento.fit(X_train, y_train)

    # Evaluar el modelo
    print("Evaluando el modelo")
    y_pred = modelo_momento.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nPrecisión del modelo para 'Momento': {accuracy:.2f}")
    print("Etiquetas en LabelEncoder de 'Momento':", le_momento.classes_)

    print("Distribución en datos de entrenamiento:")
    print(y_train.value_counts())
    print("Distribución en datos de prueba:")
    print(y_test.value_counts())
    
    # Guardar el modelo
    print("Guardando el modelo y objetos auxiliares...")
    df_food.to_pickle("templates/df_food.pkl")
    joblib.dump(modelo_momento, "templates/modelo_momento.pkl")
    joblib.dump(scaler, "templates/scaler.pkl")
    joblib.dump(le_momento, "templates/label_encoder_momento.pkl")
    joblib.dump(le_category, "templates/label_encoder_category.pkl")


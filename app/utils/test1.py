import tensorflow as tf
from keras import layers
from keras import Sequential
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Simulación de datos de entrenamiento
X_train = np.array([
    [25, 70, 1, 0, 30],  # Edad, Peso, Género (1: Masculino, 0: Femenino), Objetivo (0: Mantener, 1: Perder, 2: Ganar), Duración
    [35, 80, 0, 1, 45],
    [28, 60, 1, 2, 30],
    [22, 55, 0, 0, 40]
])

# Requerimientos nutricionales por comida (Carbohidratos, Proteínas, Grasas) para cada día
y_train = np.array([
    [250, 150, 60],  # Carbohidratos, Proteínas, Grasas
    [220, 130, 70],
    [300, 160, 80],
    [280, 140, 75]
])

# Normalización de los datos
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Normalizar las salidas (carbohidratos, proteínas y grasas)
scaler_output = MinMaxScaler()
y_train = scaler_output.fit_transform(y_train)

# Definición de la red neuronal
model = Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    layers.Dense(64, activation='relu'),
    layers.Dense(3)  # Salida: Carbohidratos, Proteínas y Grasas
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# Entrenamiento del modelo
model.fit(X_train_scaled, y_train, epochs=100)

# Predicción de nutrientes para un nuevo usuario
new_user = np.array([[30, 75, 1, 2, 7]])  # Edad, peso, género, objetivo, duración
new_user_scaled = scaler.transform(new_user)

nutrients = model.predict(new_user_scaled)
print("Predicción de nutrientes (Carbohidratos, Proteínas, Grasas):", nutrients)


from scipy.optimize import linprog

# Base de datos de alimentos (por simplicidad, solo 3 alimentos con macronutrientes)
# Cada fila es un alimento: [Carbohidratos (g), Proteínas (g), Grasas (g), Calorías (kcal)]
food_db = np.array([
    [20, 5, 10, 150],  # Alimento 1 (Ejemplo: Pollo)
    [50, 10, 2, 200],  # Alimento 2 (Ejemplo: Pasta)
    [30, 8, 5, 180]    # Alimento 3 (Ejemplo: Arroz)
])

# Requerimientos nutricionales para un nuevo usuario
# Nutrientes necesarios: [Carbohidratos, Proteínas, Grasas]
required_nutrients = [250, 150, 60]

# Coeficientes de la función objetivo (minimizar el costo total de los alimentos)
costs = np.array([2, 3, 1.5])  # Costo por 100g de cada alimento

# Restricciones: Necesitamos cumplir con los requerimientos de nutrientes
A = np.array([
    [20, 50, 30],  # Carbohidratos
    [5, 10, 8],    # Proteínas
    [10, 2, 5]     # Grasas
])

b = np.array(required_nutrients)

# Resolver el problema de optimización (mínimo costo para cumplir con los requerimientos)
res = linprog(costs, A_eq=A, b_eq=b, bounds=[(0, None), (0, None), (0, None)])

# Imprimir los resultados de la optimización
print(f"Cantidad de alimentos a consumir: {res.x}")

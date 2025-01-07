
# Requerimientos e Instalación

Este proyecto utiliza **Python**. Asegúrate de tenerlo instalado antes de comenzar.

## 1. Instalar el entorno virtual

Para crear un entorno virtual:

```bash
python -m venv venv
```

## 2. Activar el entorno virtual

Dependiendo de la terminal que utilices, activa el entorno virtual con uno de los siguientes comandos:

### Git Bash:

```bash
source venv/Scripts/activate
```

### Terminal de VSCode (Windows):

```bash
.\env\Scripts\ctivate
```

### Desactivar el entorno virtual

Para desactivar el entorno virtual en cualquier terminal:

```bash
deactivate
```

## 3. Instalar Flask

Con el entorno virtual activado, instala Flask:

```bash
pip install flask
```

## 4. Ejecutar la aplicación Flask

Para ejecutar la aplicación:

```bash
flask --app main --debug run --host=0.0.0.0
```

## 5. Instalar las dependencias

Con el entorno virtual activado y desde la raíz del proyecto, instala todas las dependencias:

```bash
pip install -r requirements.txt
```

Si no tienes el archivo `requirements.txt`, puedes instalar manualmente las dependencias con los siguientes comandos:

```bash
pip install SQLAlchemy
pip install flask_sqlalchemy
pip install psycopg2
pip install python-dotenv
pip install flask-httpauth
pip install pyjwt
pip install marshmallow-sqlalchemy
pip install flask-marshmallow
pip install Flask-migrate
pip install setuptools
pip install flasgger
```

## 6. Ejecutar migraciones

Para gestionar las migraciones de base de datos, utiliza los siguientes comandos:

### Inicializar migraciones (solo la primera vez):

```bash
flask db init
```

### Crear una nueva migración:

```bash
flask db migrate -m "detalle de la migración"
```

### Aplicar las migraciones:

```bash
flask db upgrade
```


## 7. Ejecutar comandos CLI

Este proyecto incluye varios comandos CLI registrados para facilitar la inicialización de datos en la base de datos. Se tiene que haber ejecutado las migraciones.

### Vista del plan en JSON:
A continuación se muestra un ejemplo de la respuesta JSON que devuelve la API cuando se obtiene un plan de comidas exitosamente. plan de 3 dias cada dia con desayuno, almuerzo, cena

```json
{
    "calories": 6509.625,
    "date_generation": "2025-01-03T00:38:07",
    "meals": [
        {
            "date": "2025-01-03T00:38:07",
            "day": 1,
            "foods": [
                {
                    "benefits": "Ayuda a la digestión y regula el tránsito intestinal.",
                    "calories": 36.0,
                    "carbohydrates": 8.9,
                    "category": "frutas",
                    "description": "Fruta dulce con alto contenido de fibra.",
                    "fats": 0.1,
                    "food_id": 713,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732637873/ssjun4l4luhmhhbyy1up.jpg",
                    "name": "Ciruela",
                    "proteins": 0.5,
                    "quantity": 1.0,
                    "type_quantity": "unidad"
                },
                {
                    "benefits": "Muy hidratante y bajo en calorías, ideal para climas cálidos.",
                    "calories": 15.0,
                    "carbohydrates": 3.7,
                    "category": "frutas",
                    "description": "Fruta refrescante con alto contenido de agua.",
                    "fats": 0.0,
                    "food_id": 732,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732637647/u86qs2tolsjcgqgritk6.jpg",
                    "name": "Sandía",
                    "proteins": 0.7,
                    "quantity": 1.0,
                    "type_quantity": "unidad"
                },
                {
                    "benefits": "Rico en antioxidantes, protege contra el envejecimiento celular.",
                    "calories": 35.0,
                    "carbohydrates": 6.5,
                    "category": "frutas",
                    "description": "Fruto oscuro y jugoso con alto contenido de antioxidantes.",
                    "fats": 0.6,
                    "food_id": 725,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732637663/ax6lzbldd0a2gu9e4qdr.jpg",
                    "name": "Mora",
                    "proteins": 1.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Fuente de proteínas y calcio, fortalece huesos y músculos.",
                    "calories": 380.0,
                    "carbohydrates": 29.5,
                    "category": "quesos",
                    "description": "Queso de oveja con un sabor fuerte y textura firme.",
                    "fats": 29.5,
                    "food_id": 816,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732643097/nksyogsihfc2tvjkvweb.jpg",
                    "name": "Queso de Oveja",
                    "proteins": 28.2,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Contiene grasas trans, generalmente no recomendada debido a sus efectos negativos sobre la salud cardiovascular.",
                    "calories": 747.0,
                    "carbohydrates": 0.3,
                    "category": "grasas",
                    "description": "Grasa vegetal procesada, comúnmente utilizada como sustituto de la mantequilla en la cocina",
                    "fats": 99.0,
                    "food_id": 800,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732642558/njdhhketfv18hewbluud.jpg",
                    "name": "Margarina",
                    "proteins": 0.0,
                    "quantity": 17.0,
                    "type_quantity": "gramo"
                }
            ],
            "meal_id": 91,
            "meal_type": "desayuno",
            "name": "Perder peso",
            "total_calories": 542.5,
            "total_carbohydrates": 48.9,
            "total_fats": 129.2,
            "total_proteins": 30.4
        },
        {
            "date": "2025-01-03T00:38:07",
            "day": 1,
            "foods": [
                {
                    "benefits": "Baja en grasas y rica en proteínas, ideal para dietas saludables.",
                    "calories": 120.0,
                    "carbohydrates": 0.5,
                    "category": "carnes",
                    "description": "Ave de carne magra y delicada, rica en proteínas y baja en grasas.",
                    "fats": 1.4,
                    "food_id": 676,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732632565/xl36nny6fnx2kiduydwu.jpg",
                    "name": "Perdiz",
                    "proteins": 25.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Rico en ácidos grasos omega-3, beneficia la salud del corazón y el cerebro.",
                    "calories": 37.0,
                    "carbohydrates": 7.8,
                    "category": "verduras/hortalizas",
                    "description": "Raíz de color naranja con sabor dulce y textura crujiente.",
                    "fats": 0.2,
                    "food_id": 773,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638563/psqsvkgrsklczpns00s9.jpg",
                    "name": "Zanahoria",
                    "proteins": 1.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Ayuda a controlar el colesterol, es rico en antioxidantes y mejora la salud cardiovascular.",
                    "calories": 24.0,
                    "carbohydrates": 5.2,
                    "category": "verduras/hortalizas",
                    "description": "Bulbo de sabor dulce y textura crujiente.",
                    "fats": 0.0,
                    "food_id": 754,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638663/eeyohqabuitsp5cz44it.jpg",
                    "name": "Cebolla",
                    "proteins": 1.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Rico en antioxidantes, protege la vista y mejora la salud ósea.",
                    "calories": 20.0,
                    "carbohydrates": 3.4,
                    "category": "verduras/hortalizas",
                    "description": "Hoja verde púrpura con sabor suave y textura firme.",
                    "fats": 0.2,
                    "food_id": 755,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638660/yklgr0whyui6xvqp4kvs.jpg",
                    "name": "Col lombarda",
                    "proteins": 1.9,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Alto contenido de omega-3 y proteínas, ideal para la salud cardiovascular y muscular.",
                    "calories": 96.0,
                    "carbohydrates": 0.0,
                    "category": "pescados",
                    "description": "Pescado azul magro de carne firme.",
                    "fats": 0.0,
                    "food_id": 704,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732634625/rxj7vzynbyqz67jjg2jf.jpg",
                    "name": "Trucha",
                    "proteins": 0.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                }
            ],
            "meal_id": 92,
            "meal_type": "almuerzo",
            "name": "Perder peso",
            "total_calories": 297.0,
            "total_carbohydrates": 16.9,
            "total_fats": 1.7999999999999998,
            "total_proteins": 28.9
        },
        {
            "date": "2025-01-03T00:38:07",
            "day": 1,
            "foods": [
                {
                    "benefits": "Rica en carbohidratos complejos, ideal para energía prolongada.",
                    "calories": 349.0,
                    "carbohydrates": 89.0,
                    "category": "frutos secos",
                    "description": "Fruto seco con textura suave y sabor dulce.",
                    "fats": 3.0,
                    "food_id": 737,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638447/qkifkfmxmgzdaomyfqqq.jpg",
                    "name": "Castaña",
                    "proteins": 4.7,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Fuente de grasas saludables, mejora el corazón y regula el colesterol.",
                    "calories": 499.0,
                    "carbohydrates": 4.0,
                    "category": "frutos secos",
                    "description": "Fruto seco con sabor suave y ligeramente dulce.",
                    "fats": 51.4,
                    "food_id": 734,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638455/yfvutq6roegrxdw0wkzh.jpg",
                    "name": "Almendra",
                    "proteins": 16.0,
                    "quantity": 82.26,
                    "type_quantity": "gramo"
                }
            ],
            "meal_id": 93,
            "meal_type": "cena",
            "name": "Perder peso",
            "total_calories": 759.4774,
            "total_carbohydrates": 93.0,
            "total_fats": 54.4,
            "total_proteins": 20.7
        },
        {
            "date": "2025-01-04T00:38:07",
            "day": 2,
            "foods": [
                {
                    "benefits": "Rico en antioxidantes, protege contra el envejecimiento celular.",
                    "calories": 35.0,
                    "carbohydrates": 6.5,
                    "category": "frutas",
                    "description": "Fruto oscuro y jugoso con alto contenido de antioxidantes.",
                    "fats": 0.6,
                    "food_id": 725,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732637663/ax6lzbldd0a2gu9e4qdr.jpg",
                    "name": "Mora",
                    "proteins": 1.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Rico en antioxidantes y energía rápida, ideal para la salud cardiovascular.",
                    "calories": 61.0,
                    "carbohydrates": 15.6,
                    "category": "frutas",
                    "description": "Pequeño fruto dulce y jugoso.",
                    "fats": 0.1,
                    "food_id": 733,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732637645/ao8p7akwijmvfabg6kmk.jpg",
                    "name": "Uva",
                    "proteins": 0.5,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Bajo en grasa, adecuado para personas con restricciones dietéticas.",
                    "calories": 336.0,
                    "carbohydrates": 78.6,
                    "category": "cereales y derivados",
                    "description": "Pasta hecha de trigo dura, ideal para sopas o ensaladas.",
                    "fats": 0.3,
                    "food_id": 791,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732642580/pnuyjlg8ccpl2sxmjbkm.jpg",
                    "name": "Pasta de sémola",
                    "proteins": 13.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Rica en azúcares y grasas, proporciona energía rápida, pero debe consumirse con moderación.",
                    "calories": 409.0,
                    "carbohydrates": 82.3,
                    "category": "cereales y derivados",
                    "description": "Galleta crujiente de trigo, comúnmente usada para postres o acompañamientos.",
                    "fats": 8.1,
                    "food_id": 784,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732642599/uvvy9857ngbf5rbaawta.jpg",
                    "name": "Galleta tipo María",
                    "proteins": 6.8,
                    "quantity": 1.0,
                    "type_quantity": "unidad"
                },
                {
                    "benefits": "Bajo en calorías, mejora la salud cardiovascular.",
                    "calories": 26.0,
                    "carbohydrates": 6.2,
                    "category": "frutas",
                    "description": "Fruta cítrica con sabor agridulce.",
                    "fats": 0.0,
                    "food_id": 731,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732637649/jtuzjrgstd2xjmn5hifl.jpg",
                    "name": "Pomelo",
                    "proteins": 0.6,
                    "quantity": 1.0,
                    "type_quantity": "unidad"
                }
            ],
            "meal_id": 94,
            "meal_type": "desayuno",
            "name": "Perder peso",
            "total_calories": 436.34999999999997,
            "total_carbohydrates": 189.2,
            "total_fats": 9.1,
            "total_proteins": 21.900000000000002
        },
        {
            "date": "2025-01-04T00:38:07",
            "day": 2,
            "foods": [
                {
                    "benefits": "Rica en hierro, fósforo y vitaminas, ideal para fortalecer el sistema inmune.",
                    "calories": 162.0,
                    "carbohydrates": 0.0,
                    "category": "carnes",
                    "description": "Ave pequeña con carne tierna y sabrosa, alta en proteínas y baja en grasa.",
                    "fats": 6.8,
                    "food_id": 663,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732632206/jgcylzwrwam2m17c7jaa.jpg",
                    "name": "Codorniz",
                    "proteins": 25.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Rico en vitamina C, ayuda a la circulación y a reducir la inflamación.",
                    "calories": 13.2,
                    "carbohydrates": 1.6,
                    "category": "verduras/hortalizas",
                    "description": "Hoja verde con sabor picante y fresco.",
                    "fats": 0.2,
                    "food_id": 749,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638675/clmmfopzsc6adhanfkjr.jpg",
                    "name": "Berro",
                    "proteins": 2.4,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Buena fuente de proteínas y grasas, ideal para aportar energía.",
                    "calories": 361.0,
                    "carbohydrates": 0.0,
                    "category": "carnes",
                    "description": "Parte curada del cerdo, de sabor intenso y rica en grasas, ideal para platos tradicionales.",
                    "fats": 31.6,
                    "food_id": 671,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732632571/yrwmcf2mfd1a1jjo3h2p.jpg",
                    "name": "Lacón",
                    "proteins": 19.2,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Bajo en grasas, alto en proteínas, rico en zinc y vitaminas B6 y B12.",
                    "calories": 146.0,
                    "carbohydrates": 0.0,
                    "category": "carnes",
                    "description": "Fuente magra de proteínas, con bajo contenido de grasas y un perfil rico en vitaminas B1 y B6.",
                    "fats": 6.8,
                    "food_id": 660,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732632084/tjdw1rmwsw42c3fueose.jpg",
                    "name": "Cerdo carne magra",
                    "proteins": 19.9,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Bajo en calorías, alto en vitamina C y promueve la salud cardiovascular.",
                    "calories": 12.0,
                    "carbohydrates": 1.4,
                    "category": "verduras/hortalizas",
                    "description": "Fruto de piel fina y carne firme, bajo en calorías.",
                    "fats": 0.1,
                    "food_id": 751,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638670/ptdbqlb94kuyc5rudmfk.jpg",
                    "name": "Calabacín",
                    "proteins": 1.3,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                }
            ],
            "meal_id": 95,
            "meal_type": "almuerzo",
            "name": "Perder peso",
            "total_calories": 694.2,
            "total_carbohydrates": 3.0,
            "total_fats": 45.5,
            "total_proteins": 67.8
        },
        {
            "date": "2025-01-04T00:38:07",
            "day": 2,
            "foods": [
                {
                    "benefits": "Fuente de azúcares naturales, ideal como energía rápida.",
                    "calories": 256.0,
                    "carbohydrates": 63.1,
                    "category": "frutos secos",
                    "description": "Fruta tropical seca con un alto contenido de azúcar natural.",
                    "fats": 0.6,
                    "food_id": 739,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638441/gemkpn2t0o2rzuj2kclr.jpg",
                    "name": "Dátil seco",
                    "proteins": 2.7,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Rica en carbohidratos complejos, ideal para energía prolongada.",
                    "calories": 349.0,
                    "carbohydrates": 89.0,
                    "category": "frutos secos",
                    "description": "Fruto seco con textura suave y sabor dulce.",
                    "fats": 3.0,
                    "food_id": 737,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638447/qkifkfmxmgzdaomyfqqq.jpg",
                    "name": "Castaña",
                    "proteins": 4.7,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Rico en azúcares naturales, fuente rápida de energía.",
                    "calories": 301.0,
                    "carbohydrates": 72.0,
                    "category": "frutos secos",
                    "description": "Uva deshidratada dulce y rica en azúcares naturales.",
                    "fats": 0.6,
                    "food_id": 744,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638184/fuirjq21vr53vwxwrsqz.jpg",
                    "name": "Uva Pasa",
                    "proteins": 1.9,
                    "quantity": 51.31,
                    "type_quantity": "gramo"
                }
            ],
            "meal_id": 96,
            "meal_type": "cena",
            "name": "Perder peso",
            "total_calories": 759.4431,
            "total_carbohydrates": 224.1,
            "total_fats": 4.2,
            "total_proteins": 9.3
        },
        {
            "date": "2025-01-05T00:38:07",
            "day": 3,
            "foods": [
                {
                    "benefits": "Mejora la memoria y la salud cardiovascular.",
                    "calories": 41.0,
                    "carbohydrates": 10.1,
                    "category": "frutas",
                    "description": "Pequeño fruto azul rico en antioxidantes.",
                    "fats": 0.4,
                    "food_id": 711,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732637890/jn9fl0u4l0utljbgkokb.jpg",
                    "name": "Arandano",
                    "proteins": 0.6,
                    "quantity": 1.0,
                    "type_quantity": "unidad"
                },
                {
                    "benefits": "Rico en calcio, mejora la salud dental y ósea.",
                    "calories": 306.0,
                    "carbohydrates": 22.0,
                    "category": "quesos",
                    "description": "Queso semiduro, con un sabor suave y ligeramente dulce.",
                    "fats": 22.0,
                    "food_id": 811,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732643111/vyoigk3sjpkr9gp8nnmg.jpg",
                    "name": "Edam",
                    "proteins": 26.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Rico en calcio, vitamina B12 y proteínas, ideal para la salud ósea.",
                    "calories": 374.0,
                    "carbohydrates": 25.6,
                    "category": "quesos",
                    "description": "Queso duro de sabor fuerte, originario de Italia, utilizado en pastas y pizzas.",
                    "fats": 25.6,
                    "food_id": 815,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732643099/z8hym37ncdeimtophgfk.jpg",
                    "name": "Parmesano",
                    "proteins": 36.0,
                    "quantity": 63.12,
                    "type_quantity": "gramo"
                }
            ],
            "meal_id": 97,
            "meal_type": "desayuno",
            "name": "Perder peso",
            "total_calories": 542.4788000000001,
            "total_carbohydrates": 57.7,
            "total_fats": 48.0,
            "total_proteins": 62.6
        },
        {
            "date": "2025-01-05T00:38:07",
            "day": 3,
            "foods": [
                {
                    "benefits": "Ayuda a reducir la inflamación y mejora la digestión.",
                    "calories": 16.0,
                    "carbohydrates": 3.2,
                    "category": "verduras/hortalizas",
                    "description": "Tallo comestible con aroma anisado y sabor refrescante.",
                    "fats": 0.3,
                    "food_id": 762,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638642/qvenzguhhvjpw4le5vjh.jpg",
                    "name": "Hinojo",
                    "proteins": 0.5,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Alto en proteínas y omega-3, promueve la salud del corazón y el cerebro.",
                    "calories": 158.0,
                    "carbohydrates": 0.0,
                    "category": "pescados",
                    "description": "Pescado magro de carne firme y versátil.",
                    "fats": 8.0,
                    "food_id": 682,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732634242/gsw3q7omnwyo3zwzw7ec.jpg",
                    "name": "Atún fresco",
                    "proteins": 21.5,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Bajo en grasas, excelente fuente de proteínas magras.",
                    "calories": 134.0,
                    "carbohydrates": 0.4,
                    "category": "carnes",
                    "description": "Carne magra de ave, baja en grasas y alta en proteínas, ideal para dietas ligeras.",
                    "fats": 4.9,
                    "food_id": 674,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732632568/i5tgsqidam0qchb7join.jpg",
                    "name": "Pavo pechuga",
                    "proteins": 22.0,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Bajo en grasas y alto en proteínas, ayuda al mantenimiento muscular.",
                    "calories": 82.0,
                    "carbohydrates": 0.8,
                    "category": "pescados",
                    "description": "Pescado plano de sabor suave y carne tierna.",
                    "fats": 1.7,
                    "food_id": 691,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732634652/lky7tdr1ejiukswlesv5.jpg",
                    "name": "Lenguado",
                    "proteins": 16.9,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Rica en antioxidantes, mejora la función digestiva y combate la inflamación.",
                    "calories": 25.0,
                    "carbohydrates": 2.7,
                    "category": "verduras/hortalizas",
                    "description": "Vegetal crucífero con sabor suave y textura tierna.",
                    "fats": 0.2,
                    "food_id": 757,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638655/mkdpeoyal4xvcjog6xay.jpg",
                    "name": "Coliflor",
                    "proteins": 3.2,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                }
            ],
            "meal_id": 98,
            "meal_type": "almuerzo",
            "name": "Perder peso",
            "total_calories": 415.0,
            "total_carbohydrates": 7.1000000000000005,
            "total_fats": 15.1,
            "total_proteins": 64.1
        },
        {
            "date": "2025-01-05T00:38:07",
            "day": 3,
            "foods": [
                {
                    "benefits": "Alto en proteínas, grasas saludables, y energía sostenida.",
                    "calories": 452.0,
                    "carbohydrates": 35.0,
                    "category": "frutos secos",
                    "description": "Legumbre con alto contenido de proteínas y grasas.",
                    "fats": 25.6,
                    "food_id": 736,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638450/xyxxgr4dk5gk3sdqs5dx.jpg",
                    "name": "Cacahuete",
                    "proteins": 20.4,
                    "quantity": 100.0,
                    "type_quantity": "gramo"
                },
                {
                    "benefits": "Alta en omega-3, beneficiosa para el cerebro y la salud cardiovascular.",
                    "calories": 670.0,
                    "carbohydrates": 11.2,
                    "category": "frutos secos",
                    "description": "Fruto seco con alto contenido de grasas saludables.",
                    "fats": 63.3,
                    "food_id": 741,
                    "image_url": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1732638435/bx56tetcyahemybhdrpg.jpg",
                    "name": "Nuez",
                    "proteins": 15.6,
                    "quantity": 45.89,
                    "type_quantity": "gramo"
                }
            ],
            "meal_id": 99,
            "meal_type": "cena",
            "name": "Perder peso",
            "total_calories": 759.463,
            "total_carbohydrates": 46.2,
            "total_fats": 88.9,
            "total_proteins": 36.0
        }
    ],
    "name": "Perder peso",
    "plan_id": 15,
    "status": "en progreso"
}
```

### Cargar datos de actividades físicas:

```bash
flask seed-physical-activities-db
```
Inicializa datos relacionados con actividades físicas en la base de datos.

### Cargar usuarios y perfiles de salud

```bash
flask seed-users-health-profiles-db
```
Inserta usuarios de ejemplo y sus respectivos perfiles de salud.

### Cargar alimentos predefinidos

```bash
flask seed-food-db
```
Agrega alimentos predefinidos con información detallada como calorías, proteínas y beneficios.

### Ejemplo de uso
Para poblar la base de datos con los datos iniciales, ejecuta uno o varios de estos comandos según sea necesario desde la raíz del proyecto:
```bash
flask seed-physical-activities-db
flask seed-users-health-profiles-db
flask seed-food-db
flask seed-measure-food-db

```

---

Este archivo `README.md` está estructurado para seguir las convenciones estándar y proporcionar una guía clara sobre cómo configurar y ejecutar el proyecto.

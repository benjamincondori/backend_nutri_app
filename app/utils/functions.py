
def convertir_a_json(plan_comidas):
    plan_json = {"dias": []}

    for dia, comidas in enumerate(plan_comidas, start=1):
        comidas_dia = {"dia": dia, "comidas": []}

        for momento, comida in comidas.items():
            # Ajustar nombres personalizados para cada tipo de comida
            nombres_comida = {
                "desayuno": "Nombre para el desayuno",
                "almuerzo": "Nombre para el almuerzo",
                "cena": "Nombre para la cena"
            }

            nombre_comida = nombres_comida.get(momento, "Comida desconocida")

            # Verificar que 'comida' sea un diccionario antes de intentar acceder a sus claves
            if isinstance(comida, dict):
                calorias_objetivo = comida.get("calorias_objetivo", 0)
                alimentos = []

                # Iterar sobre la lista de alimentos que está en la clave 'comida'
                for item in comida.get("comida", []):  # Aquí 'comida' es una lista
                    if isinstance(item, dict):  # Si el item es un diccionario
                        alimentos.append({
                            "alimento": item.get("alimento", "Desconocido"),
                            "cantidad": item.get("cantidad", "N/A"),
                            "unidad": item.get("unidad", "")
                        })
                    elif isinstance(item, str):  # Si el item es una cadena
                        alimentos.append({
                            "alimento": item,
                            "cantidad": "N/A",
                            "unidad": ""
                        })
            elif isinstance(comida, list):  # Si 'comida' es una lista
                calorias_objetivo = 0
                alimentos = []

                # Iterar directamente sobre la lista de alimentos
                for item in comida:  # Aquí 'comida' es una lista
                    if isinstance(item, dict):  # Si el item es un diccionario
                        alimentos.append({
                            "alimento": item.get("alimento", "Desconocido"),
                            "cantidad": item.get("cantidad", "N/A"),
                            "unidad": item.get("unidad", "")
                        })
                    elif isinstance(item, str):  # Si el item es una cadena
                        alimentos.append({
                            "alimento": item,
                            "cantidad": "N/A",
                            "unidad": ""
                        })

            else:
                # Si 'comida' no es un diccionario ni una lista, asigna valores por defecto o maneja el error
                calorias_objetivo = 0
                alimentos = []

            # Añadir la comida al día
            comidas_dia["comidas"].append({
                "nombre": nombre_comida,
                "tipo_comida": momento,
                "alimentos": alimentos
            })

        plan_json["dias"].append(comidas_dia)

    return plan_json

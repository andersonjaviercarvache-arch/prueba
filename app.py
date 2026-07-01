from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math

# Inicializamos la API con el nombre correcto de tu aplicación
app = FastAPI(title="Sistema de ingeniería de costos y control financiero - API Fotovoltaica")

# Base de datos simulada de inversores (puedes conectarlo a una DB real luego)
INVERSORES_DB = {
    "Huawei-SUN2000-5KTL": {"potencia_w": 5000, "paneles_max_por_string": 12},
    "Huawei-SUN2000-10KTL": {"potencia_w": 10000, "paneles_max_por_string": 15},
    "Victron-MultiPlus-3000": {"potencia_w": 3000, "paneles_max_por_string": 8}
}

# Modelo de datos esperado en la petición
class PeticionDimensionamiento(BaseModel):
    modelo_inversor: str
    cantidad_paneles: int

@app.post("/calcular_protecciones")
def calcular_protecciones(datos: PeticionDimensionamiento):
    # 1. Validar si el inversor existe en nuestra base de datos
    if datos.modelo_inversor not in INVERSORES_DB:
        raise HTTPException(status_code=404, detail="Modelo de inversor no encontrado")
    
    inversor = INVERSORES_DB[datos.modelo_inversor]
    
    # 2. Calcular cantidad de circuitos (Strings)
    # Se divide la cantidad de paneles entre el máximo permitido por string y se redondea hacia arriba
    cantidad_circuitos = math.ceil(datos.cantidad_paneles / inversor["paneles_max_por_string"])
    
    # 3. Calcular protecciones en DC
    fusibles_dc = cantidad_circuitos * 2
    breakers_dc = cantidad_circuitos
    
    # 4. Calcular protecciones en AC
    # I = (Potencia / Voltaje) * Factor de seguridad (1.25)
    voltaje_ac = 220
    corriente_nominal_ac = inversor["potencia_w"] / voltaje_ac
    capacidad_breaker_ac = math.ceil(corriente_nominal_ac * 1.25)
    cantidad_breakers_ac = 2 # Según tu requerimiento
    
    # 5. Retornar el JSON con los resultados
    return {
        "resumen_sistema": {
            "inversor_seleccionado": datos.modelo_inversor,
            "potencia_inversor_w": inversor["potencia_w"],
            "total_paneles": datos.cantidad_paneles,
            "total_circuitos_strings": cantidad_circuitos
        },
        "protecciones_DC": {
            "cantidad_fusibles": fusibles_dc,
            "cantidad_breakers": breakers_dc,
            "nota": "Instalación en gabinete DC"
        },
        "protecciones_AC": {
            "cantidad_breakers": cantidad_breakers_ac,
            "amperaje_recomendado_breaker": capacidad_breaker_ac,
            "voltaje_calculo": voltaje_ac,
            "nota": "Instalación en gabinete AC"
        }
    }

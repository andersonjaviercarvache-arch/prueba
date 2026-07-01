import streamlit as st
import math

# Configuración de la página
st.set_page_config(page_title="Dimensionamiento PV", layout="centered")

# Título principal estricto de tu aplicación
st.title("Sistema de ingeniería de costos y control financiero")
st.subheader("Módulo de Dimensionamiento y Protecciones")

# Base de datos interna de inversores
INVERSORES_DB = {
    "Huawei-SUN2000-5KTL": {"potencia_w": 5000, "paneles_max_por_string": 12},
    "Huawei-SUN2000-10KTL": {"potencia_w": 10000, "paneles_max_por_string": 15},
    "Huawei-SUN2000-60KTL": {"potencia_w": 60000, "paneles_max_por_string": 20},
    "Victron-MultiPlus-3000": {"potencia_w": 3000, "paneles_max_por_string": 8}
}

# Interfaz de usuario para ingresar datos
modelo_seleccionado = st.selectbox("Seleccione el modelo del inversor", list(INVERSORES_DB.keys()))
cantidad_paneles = st.number_input("Cantidad de paneles solares", min_value=1, value=10, step=1)

# Botón de cálculo
if st.button("Calcular Protecciones y Circuitos"):
    inversor = INVERSORES_DB[modelo_seleccionado]
    
    # 1. Cálculo de Strings (Circuitos)
    cantidad_circuitos = math.ceil(cantidad_paneles / inversor["paneles_max_por_string"])
    
    # 2. Protecciones DC 
    fusibles_dc = cantidad_circuitos * 2
    breakers_dc = cantidad_circuitos
    
    # 3. Protecciones AC 
    voltaje_ac = 220
    corriente_nominal_ac = inversor["potencia_w"] / voltaje_ac
    capacidad_breaker_ac = math.ceil(corriente_nominal_ac * 1.25)
    cantidad_breakers_ac = 2 
    
    # --- MOSTRAR RESULTADOS EN PANTALLA ---
    st.success("Cálculo de dimensionamiento completado")
    
    col_principal, _ = st.columns([1, 1])
    with col_principal:
        st.metric("Total de Circuitos (Strings)", cantidad_circuitos)
    
    st.divider()
    
    # Separación clara de terminales como en los gabinetes reales
    col_dc, col_ac = st.columns(2)
    
    with col_dc:
        st.write("### Terminales DC")
        st.info(f"**Fusibles DC necesarios:** {fusibles_dc}\n\n**Breakers DC necesarios:** {breakers_dc}")
        st.caption("2 fusibles y 1 breaker por cada circuito ingresando al inversor.")
        
    with col_ac:
        st.write("### Terminales AC")
        st.warning(f"**Breakers AC necesarios:** {cantidad_breakers_ac}\n\n**Amperaje recomendado:** {capacidad_breaker_ac} A")
        st.caption("Cálculo a 220V con factor de seguridad del 25%.")

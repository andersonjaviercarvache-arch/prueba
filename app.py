import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Dimensionamiento PV", layout="centered")

st.title("Sistema de ingeniería de costos y control financiero")
st.subheader("Módulo de Dimensionamiento y Protecciones")

# Opciones de la interfaz
modelos_disponibles = [
    "Huawei-SUN2000-5KTL", 
    "Huawei-SUN2000-10KTL", 
    "Huawei-SUN2000-60KTL",
    "Victron-MultiPlus-3000"
]

modelo_seleccionado = st.selectbox("Seleccione el modelo del inversor", modelos_disponibles)
cantidad_paneles = st.number_input("Cantidad de paneles solares", min_value=1, value=10, step=1)

# Botón para calcular
if st.button("Calcular Protecciones y Circuitos"):
    # Dirección de nuestra API local
    url_api = "http://127.0.0.1:8000/calcular_protecciones"
    
    # Datos que enviamos a la API
    datos_a_enviar = {
        "modelo_inversor": modelo_seleccionado,
        "cantidad_paneles": cantidad_paneles
    }
    
    try:
        # Hacemos la petición a la API
        respuesta = requests.post(url_api, json=datos_a_enviar)
        
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            
            # Mostrar resultados en pantalla
            st.success("Cálculo realizado con éxito")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Strings", resultado["total_circuitos_strings"])
            
            st.divider()
            
            col_dc, col_ac = st.columns(2)
            with col_dc:
                st.write("### Gabinete DC")
                st.write(f"- **Fusibles necesarios:** {resultado['fusibles_dc']}")
                st.write(f"- **Breakers DC necesarios:** {resultado['breakers_dc']}")
                
            with col_ac:
                st.write("### Gabinete AC")
                st.write(f"- **Breakers AC necesarios:** {resultado['breakers_ac']}")
                st.write(f"- **Amperaje recomendado:** {resultado['amperaje_breaker_ac']} A")
                
        else:
            st.error("Error al comunicarse con la API. Revisa que Uvicorn esté corriendo.")
            
    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar a la API. ¿Aseguraste ejecutar 'uvicorn api:app --reload' en otra terminal?")

import streamlit as st
import datetime
import json
import pandas as pd

# Load the archetype data from the JSON file
with open('archetypes.json', encoding='utf-8') as f:
    archetypes = json.load(f)['arquetipos']

# Load the data from the Excel file
norte = pd.read_excel('personas.xlsx', sheet_name='Norte')
sur = pd.read_excel('personas.xlsx', sheet_name='Sur')

def calculate_ming_gua(birth_year, birth_hemisphere, gender):
    if birth_hemisphere == 'HEMISFERIO NORTE':
        if gender == 'Hombre':
            min_gua = norte[norte['Yr'] == birth_year]['Hombre'].values[0]
        else:
            min_gua = norte[norte['Yr'] == birth_year]['Mujer'].values[0]
    else:
        if gender == 'Hombre':
            min_gua = sur[sur['Yr'] == birth_year]['Hombre'].values[0]
        else:
            min_gua = sur[sur['Yr'] == birth_year]['Mujer'].values[0]
    
    return min_gua

# Streamlit app
st.title("Ming Gua Calculador de Arquetipo")

# Get user input
birth_date = st.date_input(
    "Ingresa tu fecha de nacimiento",
    min_value=datetime.date(1910, 1, 1),
    max_value=datetime.date.today()
)

# Extract only the year from the birth date
birth_year = birth_date.year

birth_hemisphere = st.selectbox(
    "Selecciona el hemisferio donde naciste",
    ['HEMISFERIO NORTE', 'HEMISFERIO SUR']
)

gender = st.selectbox(
    "Selecciona tu género",
    ['Mujer', 'Hombre']
)

if st.button('Calcular Ming Gua'):
    try:
        # Calculate the Ming Gua number
        ming_gua_number = calculate_ming_gua(birth_year, birth_hemisphere, gender)
        
        st.write(f"Tu número Ming Gua es: {ming_gua_number}")

        # Find the corresponding archetype
        archetype = None
        for a in archetypes:
            if int(a['id']) == ming_gua_number:
                archetype = a
                break

        if archetype:
            st.subheader(f"Tu Arquetipo Ming Gua es: {archetype['nombre']}")
            st.write(f"### Tu orientación es: {archetype['orientacion']}")
            
            # Elementos sensoriales section with improved layout
            st.write("### Tus elementos sensoriales favorables son:")
            
            # Convert items to list and ensure we have exactly 6 items
            categorias = list(archetype['elementos_sensoriales_favorables'].items())
            # Pad with empty items if less than 6 categories
            while len(categorias) < 6:
                categorias.append(("", []))
                
            # Create two rows with three columns each
            for row in range(2):
                cols = st.columns(3)
                for col in range(3):
                    idx = row * 3 + col
                    if idx < len(categorias):
                        categoria, elementos = categorias[idx]
                        with cols[col]:
                            if categoria:  # Only display if category exists
                                st.markdown(f"**{categoria}:**")
                                for elemento in elementos:
                                    st.markdown(f"- {elemento}")
            
            st.write("### Tus ocupaciones favorables son:")
            st.write("- " + "\n- ".join(archetype['oficios_favorables']))
            
            st.write("### Tus habilidades son:")
            st.write("- " + "\n- ".join(archetype['habilidad']))
        else:
            st.write(f"Lo siento, no pudimos encontrar el arquetipo para el número Ming Gua {ming_gua_number}. Por favor verifica que todos los arquetipos estén definidos en el archivo JSON.")
    except IndexError:
        st.write("Lo siento, no pudimos encontrar el año en la base de datos. Por favor verifica que el archivo de Excel contenga todos los años necesarios.")
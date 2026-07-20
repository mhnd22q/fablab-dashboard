import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="FABLAB Machinery Dashboard", layout="wide")

df = pd.read_csv('FABLAB_cleaned.csv')

st.title("FABLAB Machinery Dashboard")
st.write("Total number of machines: " + str(len(df)))

selected_name = st.selectbox("Select machine name:", df['Name'])

machine = df[df['Name'] == selected_name].iloc[0]

st.subheader(machine['Name'])

col1, col2 = st.columns([1, 2])

with col1:
    image_path = machine['Image_File']
    if os.path.exists(image_path):
        st.image(image_path, width=250)
    else:
        st.write("No image available")

with col2:
    st.write("Machine Number: " + str(machine['#']))
    st.write("Model / Part Number: " + str(machine['Model/ Part Number']))
    st.write("Quantity: " + str(machine['Quantity']))
    st.write("Available Accessories: " + ("Yes" if machine['Available Accessories'] else "No"))
    st.write("General Features: " + str(machine['General Features']))
    st.write("Testing Main Items: " + str(machine['Testing Main Items']))
    st.write("Expected Testing Frequency per Year: " + str(machine['Expect Testing Frequency per Year']))
    
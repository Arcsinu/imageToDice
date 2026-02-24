import streamlit as st

st.title("Upload Test")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.write("File uploaded!")
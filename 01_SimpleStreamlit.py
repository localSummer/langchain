import streamlit as st

st.title("平方计算器")

number = st.slider("Select a number", min_value=0, max_value=100)

st.write(f"The square of {number} is {number ** 2}")
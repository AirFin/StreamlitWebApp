
import streamlit as st
import os

button = st.button("Click me")
if button:
    os.system("scihub-cn -d 10.1038/s41524-017-0032-0")
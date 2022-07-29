# Streamlit application that get as input a text and generate some output
import streamlit as st
import pandas as pd
import numpy as np

#Modification of the application layout
def _max_width_():
    max_width_str = f"width: 90%;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


st.title("Application")
st.subheader("Streamlit Application")

#with st.form(key="my_form"):
_max_width_()

ce, c1, ce, c2, c3 = st.columns([0.07, 1, 0.07,3, 0.07])
with c1:
    st.text_area("Customer Request:", value="", height=None, max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False)
with c2:
    st.text("Some results")

# write a title in H1 tag and a subtitle in H2 tag. with the title "Application"
# write a button that when clicked, will generate a text
# Component for uploading a jsonl file
#uploaded_file = st.file_uploader("Upload a file", type=["jsonl"])
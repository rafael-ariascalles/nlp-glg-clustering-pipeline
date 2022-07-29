# Streamlit application that get as input a text and generate some output
import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(page_title="GLG",layout="wide")

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

st.subheader("Request Analyser")


form = st.form(key="Processing")

with form:
    t = st.text_area("Customer Request:", value="",height=50, max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False)
    submited = st.form_submit_button("Submit")

st1, st2, st3, st4 = st.columns(4)
if submited:
    st.text(t)

# write a title in H1 tag and a subtitle in H2 tag. with the title "Application"
# write a button that when clicked, will generate a text
# Component for uploading a jsonl file
#uploaded_file = st.file_uploader("Upload a file", type=["jsonl"])
# Streamlit application that get as input a text and generate some output
import streamlit as st
import pandas as pd
import numpy as np
import requests
import os

st.set_page_config(page_title="GLG",layout="wide",initial_sidebar_state="expanded")

SERVICE_IP = os.getenv('SERVICE_IP')
service_endpoint = "http://{}:9898/predict".format(SERVICE_IP)
#st.write("Service endpoint: {}".format(service_endpoint))

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


st.sidebar.title("GLG")
st.sidebar.subheader("Request Analyser")
submited_text = st.sidebar.text_area("Customer Request:", value="",height=350, max_chars=1_000, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False)

if st.sidebar.button("Submit"):
    data = {"text": submited_text}
    response = requests.post(service_endpoint, json=data)
    response_object = response.json()

    #validate response code and content
    if response.status_code == 200:
        st.subheader("Customer Request")
        st.write(submited_text)
        st1, st2 = st.columns(2)    
        st1.subheader("Topics")
        st1.write(response_object["topics"])
        st2.subheader("Entities")
        st2.write(response_object["entities"])
        
    else:
        st.write("Error:", "API not responding")
# Streamlit application that get as input a text and generate some output
import streamlit as st
import pandas as pd
import numpy as np
import requests
import os

st.set_page_config(page_title="GLG",layout="wide")

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


title = '<h2 style="color:#556173">GLG Text Classification with NER and Topic Modeling</h2>'
st.markdown(title, unsafe_allow_html=True)


with st.form('details'):
    submitted_text = st.text_area('How can we help?', placeholder='Describe your needs.', height=205)
    submitted = st.form_submit_button('Submit')

if submitted:
    data = {"text": submitted_text}
    response = requests.post(service_endpoint, json=data)
    response_object = response.json()

    # validate response code and content
    if response.status_code == 200:

        # Setup columns for output and add headings
        st1, st2, st3, st4 = st.columns([1.5,1,1,1])    
        st1.markdown('<h3 style="color:#556173">Entities</span>', unsafe_allow_html=True)
        st2.markdown('<h3 style="color:#556173">Topics</span>', unsafe_allow_html=True)

        # Write entities
        st1.write(response_object["entities"])
        
        # Write top 3 topics
        st2.write(response_object["topics"][0])
        st2.markdown('<span style="color:#556173;font-size=10px"><em>*Score: lower is better</em></span>', unsafe_allow_html=True)
        st3.write(response_object["topics"][1])    
        st4.write(response_object["topics"][2])
   
        st1.subheader("Topics")
        st1.write(response_object["topics"])
        st2.subheader("Entities")
        st2.write(response_object["entities"])
        
    else:
        st.write("Error:", "API not responding")


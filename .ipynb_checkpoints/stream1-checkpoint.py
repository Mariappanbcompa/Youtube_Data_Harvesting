import streamlit as st
import numpy as np

st.markdown(
    f'<img src="https://t3.ftcdn.net/jpg/05/68/01/30/360_F_568013079_SJIBUSvwEa5s6YipDzaQC3X5Hmnc1kcI.jpg" width="1100" height="200">',
    unsafe_allow_html=True)

st.title('Youtube Data Harvesting Project ')

tab1, tab2, tab3 = st.tabs(["Load to MongoDB", "Load to MYSQL DB", "Run Quries"])

with tab1:
    option = st.selectbox(
        'How would you like to be contacted?',
        ('Email', 'Home phone', 'Mobile phone'))
    option = st.selectbox(
        'How would you like to be contactedg?',
        ('Email', 'Home phone', 'Mobilse phone'))
    
    st.button("Reset", type="primary")

    

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


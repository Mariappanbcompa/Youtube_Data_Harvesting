import streamlit as st
import mysql.connector

host = "127.0.0.1"
user = "root"
password = '1234'

try:
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        )
    mycursor = mydb.cursor()

except mysql.connector.Error as err:
    # Display an error message if the connection fails
    st.write(f"Error: {err}")




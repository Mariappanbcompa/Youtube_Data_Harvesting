import streamlit as st
import mysql.connector

host = "sql12.freesqldatabase.com"
user = "sql12653296"
password = 'UgqEDaHSNX'

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




import streamlit as st
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  #database='joins'
)
#print(mydb)
mycursor = mydb.cursor(buffered=True)






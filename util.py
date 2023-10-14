import streamlit as st
import numpy as np
from googleapiclient.discovery import build as build
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import mysql.connector
from pymongo import errors
import tab2
import testSQL as ts
import math as m
import Playlist

api_key = "AIzaSyDXLPbL851GFxL-lkqMWtA8yUYABcNSu50"
channel_id = "UCnz-ZXXER4jOvuED5trXfEA"
youtube = build('youtube','v3',developerKey = api_key)

def channeldata(ch):
    api_key = "AIzaSyDXLPbL851GFxL-lkqMWtA8yUYABcNSu50"
    channel_id = ch
    youtube = build('youtube','v3',developerKey = api_key)
    response = youtube.channels().list(
    id=channel_id,
    part='snippet,statistics,contentDetails')
    channel_data= response.execute()
    return channel_data

def mconnect():
        uri = "mongodb+srv://Marii:1234@cluster0.okcsmig.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        return client

    


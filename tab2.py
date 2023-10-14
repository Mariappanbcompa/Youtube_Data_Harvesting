import streamlit as st
import util as ut


def tab2():
    mycursor = ut.ts.mycursor
    mydb = ut.ts.mydb
    return mydb,mycursor

def tab2_data(channel_data):
    data = dict(ChanneID=channel_data['items'][0]['id'],
                channel_name=channel_data['items'][0]['snippet']['title'],
                SubscriberCount=channel_data['items'][0]['statistics']['subscriberCount'],
                ViewCount=channel_data['items'][0]['statistics']['viewCount'],
                VideoCount=channel_data['items'][0]['statistics']['videoCount'],
                Play_lits_id=channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                )
    return data


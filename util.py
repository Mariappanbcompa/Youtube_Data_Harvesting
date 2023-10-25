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
from datetime import datetime as dt
import Playlist
import re

api_key = "AIzaSyCstjF-sUzZWALRQEtqNPeEy0Z5P6_UvUc"
channel_id = "UCnz-ZXXER4jOvuED5trXfEA"
youtube = build('youtube','v3',developerKey = api_key)

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  #database='joins'
)
#print(mydb)
mycursor = mydb.cursor(buffered=True)



def channeldata(ch):

    channel_id = ch

    response = youtube.channels().list(
    id=channel_id,
    part='snippet,statistics,contentDetails')
    channel_data= response.execute()
    return channel_data

def channeldetail(channel_data):
    data = dict(ChanneID=channel_data['items'][0]['id'],
                channel_name=channel_data['items'][0]['snippet']['title'],
                SubscriberCount=channel_data['items'][0]['statistics']['subscriberCount'],
                ViewCount=channel_data['items'][0]['statistics']['viewCount'],
                VideoCount=channel_data['items'][0]['statistics']['videoCount'],
                Play_lits_id=channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                )
    return data

def mconnect():
        uri = "mongodb+srv://Marii:1234@cluster0.okcsmig.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        return client


def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)



def playls(ch_id):
    chid = ch_id
    token = ''
    plylist_ids, ch_ls, ti_ls = [], [], []
    while token != None:
        request = youtube.playlists().list(
            part="contentDetails,snippet",
            channelId=str(ch_id),
            maxResults=10,
            pageToken=token
        )
        response = request.execute()

        [plylist_ids.append(x['id']) for x in response['items']]
        [ch_ls.append(x['snippet']['channelId']) for x in response['items']]
        [ti_ls.append(x['snippet']['title']) for x in response['items']]

        try:
            token = response['nextPageToken']
        except KeyError as e:
            token = None
    playlist = {'Playlist_id': plylist_ids,
                'ChannelID': ch_ls,
                'Playlist_name': ti_ls
                }
    return playlist

def videodls(plylist_ids):

    Video_id, playlist_Id, Video_name, Published_date, View_count, Like_count, Comments_count, Duration = [], [], [], [], [], [], [], []
    for playlist in plylist_ids:
        token = ''
        videoids = []
        while token != None:
            request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist,
                maxResults=10,
                pageToken=token
            )
            response = request.execute()
            [videoids.append(item['contentDetails']['videoId']) for item in response['items']]
            try:
                token = response['nextPageToken']
            except KeyError as e:
                token = None

            batch_size = 50
            for i in range(0, len(videoids), batch_size):
                batch = videoids[i:i + batch_size]

                video_response = youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=batch
                ).execute()
                video_response


                Video_id.extend([item['id'] for item in video_response['items']])
                playlist_Id.extend([playlist for item in video_response['items']])
                Video_name.extend([item['snippet']['title'] for item in video_response['items']])
                Published_date.extend([dt.strptime(item['snippet']['publishedAt'].replace('T', ' ').replace('Z', ''),"%Y-%m-%d %H:%M:%S")
                                      .strftime("%d/%m/%Y %I:%M %p") for item in video_response['items']])
                View_count.extend([item['statistics']['viewCount'] for item in video_response['items']])
                Like_count.extend([item['statistics'].get('likeCount', None) for item in video_response['items']])
                Duration.extend([item['contentDetails']['duration'].replace('M', ':').replace('H', ':').replace('PT','').replace('S', '') for item in video_response['items']])
                Comments_count.extend([int(item['statistics'].get('commentCount', 0)) for item in video_response['items']])

    videoDetail = {'Video_id': Video_id,
                   'playlist_Id': playlist_Id,
                   'Video_name': Video_name,
                   'Published_date': Published_date,
                   'View_count': View_count,
                   'Like_count': Like_count,
                   'Comments_count': Comments_count,
                   'Duration': Duration

                   }

    return videoDetail


def Commentsd(vids):
    #st.write(vids)
    comment_id, Video_id, Comment_text, Comment_author, Comment_date = [], [], [], [], []
    for x in vids:
        token = ' '
        while token != None:
            try:
                token = reponse['nextPageToken']
            except:
                token = None

            cmt_response = youtube.commentThreads().list(
                part='snippet',
                videoId=x,
                maxResults=50,
                pageToken=token
            )

            reponse = cmt_response.execute()
            comment_id.extend([x.get('id', None) for x in reponse['items']]),
            Video_id.extend([x['snippet']['videoId'] for x in reponse['items']]),
            Comment_text.extend(
                [remove_emojis(x['snippet']['topLevelComment']['snippet'].get('textOriginal', None)) for x in
                 reponse['items']]),
            Comment_author.extend(
                [x['snippet']['topLevelComment']['snippet'].get('authorDisplayName', None) for x in reponse['items']]),
            Comment_date.extend(
                [x['snippet']['topLevelComment']['snippet'].get('publishedAt', None) for x in reponse['items']])


    cmt = {'comment_id': comment_id,
           'Video_id': Video_id,
           'Comment_text': Comment_text,
           'Comment_author': Comment_author,
           'Comment_published_date': Comment_date
           }

    return cmt

    


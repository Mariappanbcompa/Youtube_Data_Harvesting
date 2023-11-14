import streamlit as st
from datetime import datetime
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  #database='joins'
)
#print(mydb)
mycursor = mydb.cursor(buffered=True)

def datefor(cdate):
    date_obj = datetime.strptime(cdate, '%d/%m/%Y %I:%M %p')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

def loadtoSQL(channel,mydb,mycursor):

    from datetime import datetime
    datefr = lambda cdate: (datetime.strptime(cdate, '%d/%m/%Y %I:%M %p')).strftime('%Y-%m-%d %H:%M:%S')

    #channel data load

    data = channel['data']
    sqldata = tuple([int(x) if x.isnumeric() else x for x in data.values()])

    mycursor.execute(f"insert into Channel values{sqldata}")
   
    #Playlist data load
    
    data1 = channel['Playlist']
    table_name = 'playlist'
    rows = [(data1['Playlist_id'][i], data1['ChannelID'][i], data1['Playlist_name'][i]) for i in range(len(data1['Playlist_id']))]

    insert_query = f"INSERT INTO {table_name} (Playlists_id, ChannelID, Playlist_name) VALUES (%s, %s, %s);"
    mycursor.executemany(insert_query, rows)    

    #Video Details load
    data2 = channel['Video_details']
    table_name = 'video'
    rows = [(data2['Video_id'][i], data2['Playlist_id'][i], data2['Video_name'][i],
             datetime.strptime(data2['Published_date'][i], '%d/%m/%Y %I:%M %p'), int(data2['View_count'][i]),
             int(data2['Like_count'][i]), int(data2['Comment_count'][i]), data2['Duration'][i]) for i in
            range(len(data2['Video_id']))]

    insert_query = f"INSERT INTO {table_name} (Video_id, Playlist_id, Video_name, Published_date, View_count, Like_count, Comment_count, Duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    mycursor.executemany(insert_query, rows) 
    
    #Comments deatils load to SQL database.

    data3 = channel['Comment_details']
    table_name = 'comment'
    rows = [(data3['Comment_id'][i], data3['Video_id'][i], data3['Comment_text'][i], data3['Comment_author'][i],
             datefr(data3['Comment_date'][i])) for i in range(len(data3['Comment_id']))]

    insert_query = f"INSERT INTO {table_name} (Comment_id, VideoID, Comment_text, Comment_author,Comment_date) VALUES (%s, %s, %s, %s, %s);"
    mycursor.executemany(insert_query, rows)
    mydb.commit()
    






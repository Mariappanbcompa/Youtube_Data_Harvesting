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


def loadtoSQL(channel,mydb,mycursor):
    
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
    columns = tuple(channel['Video_details'].keys())
    rows = [(data2['Video_id'][i],data2['Playlist_id'][i],data2['Video_name'][i],data2['Published_date'][i],int(data2['View_count'][i]),int(data2['Like_count'][i]),int(data2['Comment_count'][i]),data2['Duration'][i]) for i in range(len(data2['Video_id']))]

    insert_query = f"INSERT INTO {table_name} (Video_id, Playlist_id, Video_name, Published_date, View_count, Like_count, Comment_count, Duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    mycursor.executemany(insert_query, rows) 
    
    #Comments deatils load to SQL database.
   
    data3 = channel['Comment_details']
    table_name = 'comment'
    rows = [(data3['Comment_id'][i],data3['Video_id'][i],data3['Comment_text'][i],data3['Comment_author'][i],datetime.strptime(data3['Comment_date'][i],'%d/%m/%Y %I:%M %p').strftime('%Y-%m-%d %H:%M:%S')) for i in range(len(data3['Comment_id']))]

    insert_query = f"INSERT INTO {table_name} (Comment_id, Video_id, Comment_text, Comment_author,Comment_date) VALUES (%s, %s, %s, %s, %s);"
    mycursor.executemany(insert_query, rows) 
    mydb.commit()
    






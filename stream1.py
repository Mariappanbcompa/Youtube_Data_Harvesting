import pandas as pd
import streamlit as st
import util as ut
from datetime import timedelta

dt = ut.dt
youtube = ut.youtube
client = ut.mconnect()

db = client.youtubedb
records = db.Channel

mycursor = ut.ts.mycursor
mydb = ut.ts.mydb
mycursor.execute("Use youtubedb")

st.title('Youtube Data Harvesting Project ')

with st.sidebar:

    st.header("List of Channel ID's")
    channel_lst = [
        "UCi8cCe02oSGS21lHrAcjogA",
        "UCjC8sqwzUme0LDJ2CeCx2Rw",
        "UCwVEhEzsjLym_u1he4XWFkg",
        "UC1VT8SUJ7yvIkE4eCzXVSNA",
        "UCNb8hHMKUSL4HigPdg2ht4A",
        "UC7LW0lREbuLEdGw37V4w7rQ",
        "UC8kFF39hsRrFfHM6-7A6APQ",
        "UCEdNYjOHEiwA1kiPoI5igKw",
        "UCY7Qlh9y1H8zuTFoFmkDwpw",
        "UCLSxqNl7wztWyTuI6eWS7VA",
        "UCT_SeKYIcxOx4DHQmlg_jEQ",
        "UClM7fatYZhgbMqpqyqHmKAw",
        "UCIqFiFqyXBegTCECeAc9O9Q",
        "UCfw5bPQzVXGt5swIOWVQz8Q"
    ]
    ls = [x['_id'] for x in records.find({"_id": {'$ne': 2}})]
    dif = list(set(channel_lst).difference(set(ls)))
    st.dataframe(pd.DataFrame({'Channel List': dif}))




tab1, tab2, tab3 = st.tabs(["Load to MongoDB", "Load to MYSQL DB", "Run Quries"])
listchennel = {}


with tab1:
    ch_id = st.text_input('Provide Channel ID')
    channel_data = ut.channeldata(ch_id)
    if ch_id:
        try:
            channel_name = channel_data['items'][0]['snippet']['title']
            st.write(f"Channel Name: {channel_name}")
            listchennel[channel_name] = channel_data
            channel_detils = ut.channeldetail(channel_data)
            st.write(channel_detils)
            playlst = ut.playls(ch_id)
            st.write(playlst)
            videodlst = ut.videodls(playlst['Playlist_id'])
            df = pd.DataFrame(videodlst)
            vids = df[df['Comment_count'] != 0]['Video_id']
            st.write(videodlst)
            commentd = ut.Commentsd(vids)
            st.write(commentd)


        except Exception as e:
            st.warning("Kindly Provide Correct Channel ID ")

        if st.button("Load Data to MongoDB", type="primary"):
            try:
                records.insert_one({"_id":ch_id,"data":channel_detils,
                                    "Playlist":playlst,
                                    "Video_details":videodlst,
                                    "Comment_details":commentd})
                st.success("Data loaded to MongoDB successfully! ")
            except ut.errors.DuplicateKeyError as e:
                st.warning("Data with the same '_id' already exists in the MongoDB collection.")
            except Exception as ex:
                st.error(f"An error occurred: {ex}")


with tab2:

    mycursor.execute("select Channel_id from Channel;")
    result = mycursor.fetchall()
    sqlls = [x[0] for x in result]
    dd = records.find({}, {"_id": True, })
    ls = [x['_id'] for x in dd]
    diff = list(set(ls).difference(set(sqlls)))

    chh_id = st.selectbox('Kindly select channel name',diff)
    if chh_id is not None:
        channel = records.find_one({"_id": chh_id})
        data = channel['data']

        st.write(data)
    else:
        st.success("SQL DB is upto date, nothing to load")
    if chh_id is not None:
        if st.button("Load Data to MYSQLDB", type="primary"):
            try:
                ut.ts.loadtoSQL(channel,mydb,mycursor)
                st.success("Data loaded to SQLDB successfully! ")
            except ut.errors.DuplicateKeyError as e:
                st.warning("Data already exists in the MySQL Database.")
            except Exception as ex:
                st.error(f"An error occurred: {ex}")


with tab3:
    option = st.selectbox(
    'Kindly select the query from the below list : ',
    ('Question_1',
    'Question_2',
    'Question_3',
    'Question_4',
    'Question_5',
    'Question_6',
    'Question_7',
    'Question_8',
    'Question_9',
    'Question_10'
    ),   index=None,
   placeholder="Select from listed query...",)

    if  option == None :
        pass
    else:
        mycursor.execute(f"select * from questions_stramlitproject where Serialno = '{option}';")
        result = mycursor.fetchall()
        st.write('Question is :', result[0][1])
        st.subheader('SQL Query')
        st.code(result[0][2])
        st.subheader('Result:')
        mycursor.execute(result[0][2])
        result1 = mycursor.fetchall()
        columns = [desc[0] for desc in mycursor.description]
        df = pd.DataFrame(result1, columns=columns)
        if 'Average_Duration' in df.columns:
            df['Average_Duration'] = df['Average_Duration'].astype(str)
        else:
            pass
        st.dataframe(df)



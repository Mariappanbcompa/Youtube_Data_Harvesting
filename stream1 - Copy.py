import streamlit as st
import util as ut


youtube = ut.youtube
client = ut.mconnect()

db = client.e18m10
records = db.YoutubeDB

mycursor = ut.ts.mycursor
mydb = ut.ts.mydb
mycursor.execute("use youtubedb;")


st.title('Youtube Data Harvesting Project ')

with st.sidebar:
    st.header("List of Channel ID's")
    "UCnz-ZXXER4jOvuED5trXfEA"
    "UCCktnahuRFYIBtNnKT5IYyg"
    "UCPIM-Ev-sEJ_aEcpDCndqUQ"
    "UC8kFF39hsRrFfHM6-7A6APQ"
    "UCShlVe9nx6m2T4I5Nn-9dbw"
    "UCe1XwK0bvZ0kYAgPWipKt7A"
    "UCW9ZN276XO_RjG836gv7HOQ"
    "UCa1s7iQUX6JBnkUrUkEknOg"
    "UCVLbzhxVTiTLiVKeGV7WEBg"
    "UCChmJrVa8kDg05JfCmxpLRw"



tab1, tab2, tab3 = st.tabs(["Load to MongoDB", "Load to MYSQL DB", "Run Quries"])
listchennel = {}
with tab1:
    ch_id = st.text_input('Provide Channel ID')
    channel_data = ut.channeldata(ch_id)
    if ch_id:
        try:
            channel_name = channel_data['items'][0]['snippet']['title']
            st.write(f"Channel Name: {channel_name}")
            st.write(channel_data)
            listchennel[channel_name] = channel_data
        except Exception as e:
            st.warning("Kindly Provide Correct Channel ID")

        if st.button("Load Data to MongoDB", type="primary"):
            try:
                records.insert_one({"_id":ch_id,"data":channel_data})
                st.success("Data loaded to MongoDB successfully! ")
            except ut.errors.DuplicateKeyError as e:
                st.warning("Data with the same '_id' already exists in the MongoDB collection.")
            except Exception as ex:
                st.error(f"An error occurred: {ex}")


with tab2:

    mycursor.execute("select ChannelID from channel;")
    result = mycursor.fetchall()
    sqlls = [x[0] for x in result]
    dd = records.find({}, {"_id": True, })
    ls = [x['_id'] for x in dd]
    diff = list(set(ls).difference(set(sqlls)))

    chh_id = st.selectbox('Kindly select channel name',diff)
    if chh_id is not None:
        channel = records.find_one({"data.items.id": chh_id})
        channel1 = channel['data']
        data = ut.tab2.tab2_data(channel1)
        st.write(data)
    else:
        st.success("SQL DB is upto date, nothing to load")
    if chh_id is not None:
        if st.button("Load Data to MYSQLDB", type="primary"):
            try:
                sqldata = tuple([int(x) if x.isnumeric() else x for x in data.values()])
                mycursor.execute("use youtubedb;")
                mycursor.execute(f"insert into channel values{sqldata}")
                mydb.commit()
                st.success("Data loaded to SQLDB successfully! ")
            except ut.errors.DuplicateKeyError as e:
                st.warning("Data already exists in the MySQL Database.")
            except Exception as ex:
                st.error(f"An error occurred: {ex}")





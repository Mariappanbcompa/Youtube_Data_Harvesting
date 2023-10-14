

def playls(ch_id,youtube,m,client):
    request = youtube.playlists().list(
        part="contentDetails,snippet",
        channelId=str(ch_id),
        maxResults=10
    )
    response = request.execute()
    id_ls = []
    ch_ls = []
    ti_ls = []
    ran = 10
    for x in range(ran):
        id_ls.append([response['items'][x].get('id')][0])
        ch_ls.append([response['items'][x]['snippet'].get('channelId')][0])
        ti_ls.append([response['items'][x]['snippet'].get('title')][0])
    pages = m.ceil(response['pageInfo']['totalResults'] / response['pageInfo']['resultsPerPage'])
    nextpage = [response.get('nextPageToken')]
    for x in range(1, pages):
        request = youtube.playlists().list(
            part="contentDetails,snippet",
            channelId="UCnz-ZXXER4jOvuED5trXfEA",
            maxResults=10,
            pageToken=str(nextpage[0])
        )
        response = request.execute()

    if response['pageInfo']['totalResults'] > 10:
        ran = response['pageInfo']['totalResults'] - response['pageInfo']['resultsPerPage']
    else:
        ran = 10

    for x in range(ran):
        id_ls.append([response['items'][x].get('id')][0])
        ch_ls.append([response['items'][x]['snippet'].get('channelId')][0])
        ti_ls.append([response['items'][x]['snippet'].get('title')][0])
    Playlist = {'Playlist_id': id_ls,
                'Channel_id': ch_ls,
                'Playlist_Name': ti_ls}
    return  Playlist

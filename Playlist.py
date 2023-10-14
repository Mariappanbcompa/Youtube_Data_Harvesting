

def playls(ch_id,youtube,m):
    chid = ch_id
    request = youtube.playlists().list(
        part="contentDetails,snippet",
        channelId=str(chid),
        maxResults=10
    )
    response = request.execute()
    id_ls = []
    ch_ls = []
    ti_ls = []
    total = response['pageInfo']['totalResults']
    if total <= 10:
        ran = total
    else:
        ran = 10
        total = total-10
    for x in range(ran):
        id_ls.append([response['items'][x].get('id')][0])
        ch_ls.append([response['items'][x]['snippet'].get('channelId')][0])
        ti_ls.append([response['items'][x]['snippet'].get('title')][0])

    pages = m.ceil(response['pageInfo']['totalResults'] / response['pageInfo']['resultsPerPage'])
    nextpage = response.get('nextPageToken')



    if nextpage is None:
        Playlist = {'Playlist_id': id_ls,
                    'Channel_id': ch_ls,
                    'Playlist_Name': ti_ls}
        return  Playlist
    else:
        for x in range(1, pages):
            request = youtube.playlists().list(
                part="contentDetails,snippet",
                channelId=str(chid),
                maxResults=10,
                pageToken=str(nextpage)
            )
            response = request.execute()

            if total <= 10:
                ran = total
            else:
                ran = 10
                total = total - 10

            for x in range(ran):
                id_ls.append([response['items'][x].get('id')][0])
                ch_ls.append([response['items'][x]['snippet'].get('channelId')][0])
                ti_ls.append([response['items'][x]['snippet'].get('title')][0])
            nextpage = response.get('nextPageToken')

        Playlist = {'Playlist_id': id_ls,
                    'Channel_id': ch_ls,
                    'Playlist_Name': ti_ls}
        return  Playlist


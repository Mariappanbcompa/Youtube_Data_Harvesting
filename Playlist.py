

def playls(ch_id,youtube):
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

def videodls(plylist_ids,youtube,dt):

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
                Comments_count.extend([item['statistics'].get('commentCount', None) for item in video_response['items']])

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

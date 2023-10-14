
def Videodetails(youtube,playlistId):
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlistId
    )
    response = request.execute()
    return response

def details():

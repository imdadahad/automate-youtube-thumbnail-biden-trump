import os

from googleapiclient.http import MediaFileUpload
import google_auth_oauthlib.flow
import googleapiclient.discovery

class YouTubeClient(object):
    def __init__(self, credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube_client = youtube_client

    def set_thumbnail(self, video_id, thumbnail):
        request = self.youtube_client.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail)
        )
        response = request.execute()

        return response

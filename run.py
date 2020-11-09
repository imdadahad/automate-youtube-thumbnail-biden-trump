import requests

from PIL import Image, ImageDraw, ImageFont
from clients.youtube_client import YouTubeClient

IMAGE_INPUT_FILE = './trump_biden.png'
IMAGE_OUTPUT_FILE = './trump_biden_generated.png'
OPENSANS_FONT_FILE = './fonts/OpenSans-ExtraBold.ttf'
YOUTUBE_DATA_API_CREDENTIALS_LOCATION = './creds/client_secret.json'

LAST_UPDATED_URL = "https://interactive.guim.co.uk/2020/11/us-general-election-data/prod/last_updated.json"
VOTE_COUNT_URL = "https://interactive.guim.co.uk/2020/11/us-general-election-data/prod/data-out/{}/president_details.json"

YOUTUBE_VIDEO_ID = "9c8P6VuymdE"


def get_election_vote_counts():
    print("Getting vote counts for the campaign")
    last_updated_response_json = requests.get(LAST_UPDATED_URL).json()
    last_updated_time = last_updated_response_json['time']
    latest_counts_response_json = requests.get(VOTE_COUNT_URL.format(last_updated_time)).json()

    biden_vote_count = latest_counts_response_json['US']['candidates'][0]['votes']
    trump_vote_count = latest_counts_response_json['US']['candidates'][1]['votes']

    print("Successfully retrieved the vote counts")

    return biden_vote_count, trump_vote_count


def create_thumbnail(biden_vote_count, trump_vote_count):
    print("Creating the thumbnail")
    image = Image.open(IMAGE_INPUT_FILE)
    font = ImageFont.truetype(OPENSANS_FONT_FILE, 80)
    drawing = ImageDraw.Draw(image)
    drawing.text((130, 480), str(biden_vote_count), font=font, fill='#FFFFFF')
    drawing.text((770, 480), str(trump_vote_count), font=font, fill='#FFFFFF')
    image.save(IMAGE_OUTPUT_FILE)

    print(f"Successfully generated the image and saved to {IMAGE_OUTPUT_FILE}")


def set_thumbnail_for_youtube_video(video_id, thumbnail):
    youtube_client = YouTubeClient(YOUTUBE_DATA_API_CREDENTIALS_LOCATION)
    response = youtube_client.set_thumbnail(video_id, thumbnail)
    print(response)


def run():
    # Get current vote counts for trump and biden
    biden_vote_count, trump_vote_count = get_election_vote_counts()
    # Create/edit thumbnail image that will show the vote counts
    create_thumbnail(biden_vote_count, trump_vote_count)
    # Upload that thumbnail to your YouTube video
    set_thumbnail_for_youtube_video(YOUTUBE_VIDEO_ID, IMAGE_OUTPUT_FILE)


if __name__ == '__main__':
    run()



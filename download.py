from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import os

# Set up the API key and YouTube channel ID
api_key = os.environ["GOOGLE_API_KEY"]

channel_id = 'UCrL_KQsmbfWyyUfwRezAEIA'  # Replace with the channel ID

youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_ids(channel_id):
    video_ids = []
    request = youtube.search().list(part='id', channelId=channel_id, maxResults=50, type='video')
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['id']['videoId'])

    return video_ids

def download_transcripts(video_ids):
    for video_id in video_ids:
        try:
            # Get the transcript for each video
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_generated_transcript(['en'])

            # Save the transcript
            with open(f"{video_id}.txt", "w") as file:
                for line in transcript.fetch():
                    file.write(f"{line['text']}\n")
            print(f"Transcript for {video_id} downloaded.")
        except Exception as e:
            print(f"Could not download transcript for video {video_id}: {str(e)}")

video_ids = get_video_ids(channel_id)
download_transcripts(video_ids)

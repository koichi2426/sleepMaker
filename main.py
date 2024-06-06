import os
from moviepy.editor import *
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# YouTube APIのサービス名とバージョンを定義
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
# 認証時に要求する権限のスコープを定義
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
# クライアントの秘密情報が含まれるJSONファイルへのパスを定義
CLIENT_SECRETS_FILE = r"json_folder/client_secret_897757286150-possg305lj69rbl5vvaiju921e4n0j2s.apps.googleusercontent.com.json"

# 認証関数を定義
def authenticate():
    # OAuth2認証のフローを管理
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # ローカルサーバーを使用して認証情報を取得
    credentials = flow.run_local_server(port=0)
    # 認証情報を使用してAPIサービスを構築
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

# ビデオアップロード関数を定義
def upload_video(youtube, file_path, title, description, category):
    # アップロードリクエストを作成
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category
            },
            "status": {
                "privacyStatus": "public"  # プライバシーステータスをpublicに固定
            }
        },
        # メディアファイルとしてアップロード
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if 'id' in response:
            print(f"Video id '{response['id']}' was successfully uploaded.")
        else:
            print("The upload failed with an unexpected response:", response)

# 動画作成関数を定義
def create_video(image_path, audio_path, output_path, duration_minutes):
    # Convert duration from minutes to seconds
    duration = duration_minutes * 60

    # Load the image and audio files
    image_clip = ImageClip(image_path).set_duration(duration)
    audio_clip = AudioFileClip(audio_path)

    # Calculate the number of loops required for the audio
    audio_duration = audio_clip.duration
    loops = int(duration / audio_duration) + 1

    # Loop the audio to match the duration of the video
    audio_clip = concatenate_audioclips([audio_clip] * loops).subclip(0, duration)

    # Set the audio to the image clip
    video_clip = image_clip.set_audio(audio_clip)

    # Write the result to an mp4 file
    video_clip.write_videofile(output_path, fps=24)

# メイン部分
if __name__ == "__main__":
    # 固定のフォルダパス
    image_folder = 'image_folder'
    audio_folder = 'audio_folder'
    output_folder = 'output_folder'

    # ターミナルから情報を入力
    duration_minutes = int(input("動画の長さ（分）を入力してください: "))
    title = input("動画のタイトルを入力してください: ")
    description = input("動画の説明を入力してください: ")
    category = "10"  # 音楽カテゴリのIDを固定

    # Get the image and audio files (assuming there's only one of each in the folder)
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.webp')]
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.wav')]

    if image_files and audio_files:
        image_path = os.path.join(image_folder, image_files[0])
        audio_path = os.path.join(audio_folder, audio_files[0])
        output_path = os.path.join(output_folder, 'output_video.mp4')

        # Create the video
        create_video(image_path, audio_path, output_path, duration_minutes)

        # YouTubeアップロードのための認証
        youtube = authenticate()

        # ビデオをアップロード
        upload_video(youtube, output_path, title, description, category)
    else:
        print("No image or audio files found in the specified folders.")

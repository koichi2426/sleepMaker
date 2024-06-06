import os
from moviepy.editor import *

def create_thumbnail(image_path, text, font, fontsize, color, position, output_path):
    # 画像ファイルを読み込む
    image_clip = ImageClip(image_path)
    
    # 画像にテキストを追加する
    txt_clip = TextClip(text, fontsize=fontsize, color=color, font=font, size=image_clip.size)
    txt_clip = txt_clip.set_position(position).set_duration(image_clip.duration)

    # テキストを画像にオーバーレイする
    composite_clip = CompositeVideoClip([image_clip, txt_clip])
    
    # 結果を保存する
    composite_clip.save_frame(output_path)

def create_video_with_thumbnail(image_path, audio_path, output_path, duration_minutes, text, font, fontsize, color, position):
    # 分を秒に変換する
    duration = duration_minutes * 60

    # テキスト付きのサムネイルを作成する
    thumbnail_path = "thumbnail_with_text.png"
    create_thumbnail(image_path, text, font, fontsize, color, position, thumbnail_path)
    
    # 修正された画像とオーディオファイルを読み込む
    image_clip = ImageClip(thumbnail_path).set_duration(duration)
    audio_clip = AudioFileClip(audio_path)

    # オーディオのループ回数を計算する
    audio_duration = audio_clip.duration
    loops = int(duration / audio_duration) + 1

    # オーディオをループして動画の長さに合わせる
    audio_clip = concatenate_audioclips([audio_clip] * loops).subclip(0, duration)

    # 画像クリップにオーディオを設定する
    video_clip = image_clip.set_audio(audio_clip)

    # 結果をmp4ファイルとして書き出す
    video_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

# パスと動画の長さを定義する
image_folder = 'image_folder'
audio_folder = 'audio_folder'
output_folder = 'output_folder'
duration_minutes = 1  # 動画の長さ（分）

# サムネイルに追加するテキストの詳細をユーザーから入力する（デフォルト値を設定）
text = input("サムネイルに追加するテキストを入力してください（デフォルト: '睡眠BGM'）: ") or "睡眠BGM"
font = input("フォントを入力してください（デフォルト: 'Arial'）: ") or "Arial"
fontsize = input("フォントサイズを入力してください（デフォルト: 70）: ") or 70
fontsize = int(fontsize)  # フォントサイズを整数に変換
color = input("テキストの色を入力してください（デフォルト: 'white'）: ") or "white"
position = input("テキストの位置を入力してください（デフォルト: 'center'）: ") or "center"

# 画像とオーディオファイルを取得する（フォルダに1つだけあると仮定）
image_files = [f for f in os.listdir(image_folder) if f.endswith('.webp') or f.endswith('.png')]
audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3') or f.endswith('.wav')]

if image_files and audio_files:
    image_path = os.path.join(image_folder, image_files[0])
    audio_path = os.path.join(audio_folder, audio_files[0])
    output_path = os.path.join(output_folder, 'output_video.mp4')

    # サムネイル付きの動画を作成する
    create_video_with_thumbnail(image_path, audio_path, output_path, duration_minutes, text, font, fontsize, color, position)
else:
    print("指定されたフォルダに画像またはオーディオファイルが見つかりません。")

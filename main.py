import os
from moviepy.editor import *

def create_thumbnail(image_path, text, font, fontsize, color, position, output_path, weight):
    # 画像ファイルを読み込む
    image_clip = ImageClip(image_path)
    
    # テキストのフォントファイルを設定する
    font_file = font
    if weight == 'bold':
        font_file = font.replace('.ttf', '-Bold.ttf')
    
    # テキストに影を付ける
    txt_shadow = TextClip(text, fontsize=fontsize, color='black', font=font_file)
    if isinstance(position, tuple):
        shadow_position = (position[0] + 2, position[1] + 2)
    else:
        shadow_position = position
    txt_shadow = txt_shadow.set_position(shadow_position).set_duration(image_clip.duration)
    
    # テキストクリップを作成する
    txt_clip = TextClip(text, fontsize=fontsize, color=color, font=font_file)
    txt_clip = txt_clip.set_position(position).set_duration(image_clip.duration)
    
    # 画像にテキストと影をオーバーレイする
    composite_clip = CompositeVideoClip([image_clip, txt_shadow, txt_clip])
    
    # 結果を保存する
    composite_clip.save_frame(output_path)

def create_video_with_thumbnail(image_path, audio_path, output_path, duration_minutes, text, font, fontsize, color, position, weight):
    # 分を秒に変換する
    duration = duration_minutes * 60

    # テキスト付きのサムネイルを作成する
    thumbnail_path = "thumbnail_with_text.png"
    create_thumbnail(image_path, text, font, fontsize, color, position, thumbnail_path, weight)
    
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

# サムネイルに追加するテキストの詳細をユーザーから入力する（デフォルト値を設定）
text = input("サムネイルに追加するテキストを入力してください（デフォルト: 'Fantastic BGM'）: ") or "Fantastic BGM"
font = input("フォントを入力してください（デフォルト: 'Papyrus' または 'Brush Script MT'）: ") or "Papyrus"
fontsize = input("フォントサイズを入力してください（デフォルト: 150）: ") or 150
fontsize = int(fontsize)  # フォントサイズを整数に変換
color = input("テキストの色を入力してください（デフォルト: 'lightblue'）: ") or "lightblue"
position_input = input("テキストの位置を入力してください（デフォルト: 'center'）: ") or "center"
weight = input("テキストの太さを入力してください（デフォルト: 'regular' または 'bold'）: ") or "regular"
duration_minutes = input("動画の長さを分単位で入力してください（デフォルト: 1）: ") or 1
duration_minutes = int(duration_minutes)

# 位置をタプルに変換する（例: 'center' -> ('center', 'center')）
position_mapping = {
    'center': 'center',
    'top': ('center', 'top'),
    'bottom': ('center', 'bottom'),
    'left': ('left', 'center'),
    'right': ('right', 'center')
}
position = position_mapping.get(position_input, 'center')

# 画像とオーディオファイルを取得する（フォルダに1つだけあると仮定）
image_files = [f for f in os.listdir(image_folder) if f.endswith('.webp') or f.endswith('.png')]
audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3') or f.endswith('.wav')]

if image_files and audio_files:
    image_path = os.path.join(image_folder, image_files[0])
    audio_path = os.path.join(audio_folder, audio_files[0])
    output_path = os.path.join(output_folder, 'output_video.mp4')

    # サムネイル付きの動画を作成する
    create_video_with_thumbnail(image_path, audio_path, output_path, duration_minutes, text, font, fontsize, color, position, weight)
else:
    print("指定されたフォルダに画像またはオーディオファイルが見つかりません。")

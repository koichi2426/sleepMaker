import os
from moviepy.editor import *

def create_thumbnail(image_path, text, font, fontsize, color, position, output_path, weight):
    image_clip = ImageClip(image_path)
    
    font_file = font
    if weight == 'bold':
        font_file = font.replace('.ttf', '-Bold.ttf')
    
    txt_shadow = TextClip(text, fontsize=fontsize, color='black', font=font_file)
    if isinstance(position, tuple):
        shadow_position = (position[0] + 2, position[1] + 2)
    else:
        shadow_position = position
    txt_shadow = txt_shadow.set_position(shadow_position).set_duration(image_clip.duration)
    
    txt_clip = TextClip(text, fontsize=fontsize, color=color, font=font_file)
    txt_clip = txt_clip.set_position(position).set_duration(image_clip.duration)
    
    composite_clip = CompositeVideoClip([image_clip, txt_shadow, txt_clip])
    composite_clip.save_frame(output_path)

def create_video_with_thumbnail(image_path, audio_path, output_path, duration_minutes, text, font, fontsize, color, position, weight):
    duration = duration_minutes * 60
    thumbnail_path = "thumbnail_with_text.png"
    create_thumbnail(image_path, text, font, fontsize, color, position, thumbnail_path, weight)
    
    image_clip = ImageClip(thumbnail_path).set_duration(duration)
    audio_clip = AudioFileClip(audio_path)

    audio_duration = audio_clip.duration
    loops = int(duration / audio_duration) + 1
    audio_clip = concatenate_audioclips([audio_clip] * loops).subclip(0, duration)

    video_clip = image_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

image_folder = 'image_folder'
audio_folder = 'audio_folder'
output_folder = 'output_folder'

# 利用可能なフォントのリスト
available_fonts = [
    "Papyrus", 
    "Brush Script MT", 
    "Arial", 
    "Times New Roman", 
    "Comic Sans MS"
]

# フォントのリストを番号付きで表示
print("利用可能なフォント:")
for i, font in enumerate(available_fonts):
    print(f"{i + 1}. {font}")

# フォントを番号で選択
font_choice = int(input("フォントを番号で選択してください: ")) - 1
font = available_fonts[font_choice]

text = input("サムネイルに追加するテキストを入力してください（デフォルト: 'Fantastic BGM'）: ") or "Fantastic BGM"
fontsize = input("フォントサイズを入力してください（デフォルト: 150）: ") or 150
fontsize = int(fontsize)
color = input("テキストの色を入力してください（デフォルト: 'lightblue'）: ") or "lightblue"
position_input = input("テキストの位置を入力してください（デフォルト: 'center'）: ") or "center"
weight = input("テキストの太さを入力してください（デフォルト: 'regular' または 'bold'）: ") or "regular"
duration_minutes = input("動画の長さを分単位で入力してください（デフォルト: 1）: ") or 1
duration_minutes = int(duration_minutes)

position_mapping = {
    'center': 'center',
    'top': ('center', 'top'),
    'bottom': ('center', 'bottom'),
    'left': ('left', 'center'),
    'right': ('right', 'center')
}
position = position_mapping.get(position_input, 'center')

image_files = [f for f in os.listdir(image_folder) if f.endswith('.webp') or f.endswith('.png')]
audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3') or f.endswith('.wav')]

if image_files and audio_files:
    image_path = os.path.join(image_folder, image_files[0])
    audio_path = os.path.join(audio_folder, audio_files[0])
    output_path = os.path.join(output_folder, 'output_video.mp4')

    create_video_with_thumbnail(image_path, audio_path, output_path, duration_minutes, text, font, fontsize, color, position, weight)
else:
    print("指定されたフォルダに画像またはオーディオファイルが見つかりません。")

"""
    从视频中提取音频
"""

from moviepy.editor import AudioFileClip

audio_clip = AudioFileClip("./src/demo02.mp4")
audio_clip.write_audiofile("./result/demo02.mp3")

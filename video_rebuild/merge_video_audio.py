"""
    合并视频和音频
"""

from moviepy.editor import AudioFileClip, VideoFileClip

src_video_path = "./result/demo02_out.mp4"
src_audio_path = "./result/demo02.mp3"

audio_clip = AudioFileClip(src_audio_path)
video_clip = VideoFileClip(src_video_path)

out_video = video_clip.set_audio(audio_clip)
out_video.write_videofile("./result/output.mp4")

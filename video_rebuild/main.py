# -*- coding: utf-8 -*-


"""
    加载源视频，逐帧处理后，输出新的视频
"""

import os
import argparse
from moviepy.editor import AudioFileClip, VideoFileClip

import add_path
from handle_frame import generate_new_video


def extract_audio(video_path, audio_path="./result/audio.mp3"):
    """
        从视频中提取音频
    """
    audio_clip = AudioFileClip(video_path)
    audio_clip.write_audiofile(audio_path)


def merge_video_audio(video_path="./result/no_audio.mp4", audio_path="./result/audio.mp3",
                      output_path="./result/output.mp4"):
    """
        合并视频和音频
    """
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)

    out_video = video_clip.set_audio(audio_clip)
    out_video.write_videofile(output_path)


def run(src_video_path, target_path, save_frame):
    if not os.path.exists("./video_rebuild/result/"):
        os.makedirs("./video_rebuild/result/")
        os.makedirs("./video_rebuild/result/frames")
    frame_dir = "./video_rebuild/result/frames"
    if os.path.exists(frame_dir):
        for file_name in os.listdir(frame_dir):
            file_path = os.path.join(frame_dir, file_name)
            os.remove(file_path)

    # 提取音频
    audio_path = "./video_rebuild/result/audio.mp3"
    extract_audio(src_video_path, audio_path)

    # 逐帧处理视频
    clip = VideoFileClip(src_video_path)
    fps = clip.fps
    del clip
    no_audio_path = "./video_rebuild/result/no_audio.mp4"
    generate_new_video(src_video_path, no_audio_path, fps, save_frame)

    # 合并音频视频
    merge_video_audio(no_audio_path, audio_path, target_path)

    # 删除中间结果
    os.remove(audio_path)
    os.remove(no_audio_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, default="./video_rebuild/src/demo03.mp4", help="source video path")
    parser.add_argument("--save-path", type=str, default="./result/output.mp4", help="result save path")
    parser.add_argument("--save-frame", action="store_true", help="save every input frame and output frame")
    opts = parser.parse_args()

    run(opts.video, opts.save_path, opts.save_frame)

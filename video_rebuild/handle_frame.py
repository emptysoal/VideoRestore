"""
    逐帧处理，并生成新的视频
"""
import os

import cv2 as cv
from tqdm import tqdm

from inference_dhd import ImageRestorer

# 构建图像修复管理器
restorer = ImageRestorer()


def edit_frame(frame, frame_idx, save_frame):
    """
        对视频的每一帧进行处理
    """
    # out_frame = cv.GaussianBlur(frame, (5, 5), 1)
    # font = cv.FONT_HERSHEY_SIMPLEX
    # out_frame = cv.putText(frame, "Output", (20, 40), font, 1, (0, 0, 255), 2, cv.LINE_AA)

    # 使用超分辨率模型转换视频帧
    out_frame = restorer.inference(frame)

    if save_frame:
        src_frame_path = os.path.join("./video_rebuild/result/frames", "%s_src.jpg" % frame_idx)
        tgt_frame_path = os.path.join("./video_rebuild/result/frames", "%s_tgt.jpg" % frame_idx)
        cv.imwrite(src_frame_path, frame)
        cv.imwrite(tgt_frame_path, out_frame)

    return out_frame


def generate_new_video(src_video_path, target_path="./result/no_audio.mp4", fps=29, save_frame=False):
    """
        读取传入的视频，对每一帧处理后，输出新的视频
    """
    cap = cv.VideoCapture(src_video_path)

    fourcc = cv.VideoWriter_fourcc("m", "p", "4", "v")
    video_fps = int(cap.get(5))
    video_width = int(cap.get(3))
    video_height = int(cap.get(4))
    video_frame_cnt = int(cap.get(7))
    base_info = {
        "帧数": video_frame_cnt,
        "FPS": video_fps,
        "分辨率": "%sx%s" % (video_width, video_height)
    }
    print("源视频基本信息：", base_info)

    out_video_writer = cv.VideoWriter(
        target_path,
        fourcc,
        fps,
        (video_width, video_height)
    )

    pbar = tqdm(range(video_frame_cnt))
    for frame_num in pbar:
        pbar.set_description("Handle frame")
        ret, frame = cap.read()

        if ret:
            img_flip = edit_frame(frame, frame_num + 1, save_frame)
            out_video_writer.write(img_flip)
        else:
            break


if __name__ == '__main__':
    video_path_test = "./src/demo02.mp4"
    video_output_path = "./result/demo02_out.mp4"
    generate_new_video(video_path_test, video_output_path)

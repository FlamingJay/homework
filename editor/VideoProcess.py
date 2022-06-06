from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import afx, AudioFileClip, ImageClip, CompositeVideoClip
import os, sys


def single_process(args):
    video_file, name, background_music, background_pic, save_path, width, height = args
    video = VideoFileClip(video_file)
    duration = video.duration

    # 加背景乐
    if background_music is not None:
        video = video.without_audio()

        audio_clip = AudioFileClip(background_music)
        audio = afx.audio_loop(audio_clip, duration=duration)
        video = video.set_audio(audio)
    # 加背景图
    if background_pic is not None:
        video = video.set_position('center')
        background_clip = ImageClip(background_pic)
        background_clip = background_clip.set_pos('center').set_duration(duration)
        # 编辑图片的尺寸
        background_clip = background_clip.resize((width, height))
        # 叠层
        video = CompositeVideoClip([background_clip, video])

    if save_path is not None:
        video.write_videofile(save_path + "\\" + name)
    else:
        video.write_videofile(os.path.dirname(sys.executable) + "\\" + name)

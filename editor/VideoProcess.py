from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import afx, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
import moviepy.video.fx.all as vfx
import os, sys


def single_process(args):
    video_file, name, background_music, volume, audio_off, background_pic, background_pic_rate, \
    save_path, crop_x_start, crop_y_start, crop_x_end, crop_y_end, logo, front, end = args

    video = VideoFileClip(video_file)
    video = video.subclip(front, video.duration - end)

    # 进行裁剪
    if (crop_x_end - crop_x_start > 0) and (crop_y_end - crop_y_start > 0):
        video = (video.fx(vfx.crop, crop_x_start, crop_y_start, crop_x_end, crop_y_end))
    duration = video.duration
    video = video.set_position('center')

    # 加背景乐
    if background_music is not None:
        # 要添加的音频
        audio_clip = AudioFileClip(background_music)
        audio = afx.audio_loop(audio_clip, duration=duration)
        audio = audio.volumex(volume / 100)

        if audio_off:
            video = video.without_audio()
            video = video.set_audio(audio)
        else:
            # 原来的音频
            video_audio_clip = video.audio
            video = video.set_audio(CompositeAudioClip([video_audio_clip, audio]))

    # 加背景图
    if background_pic is not None:
        background_clip = ImageClip(background_pic)
        background_clip = background_clip.set_pos('center').set_duration(duration)
        back_size = background_clip.size

    # 加水印
    if logo is not None:
        water_clip = ImageClip(logo)
        # todo: logo的位置
        water_clip = water_clip.set_pos('center').set_duration(duration)

    if (background_pic is not None) and (logo is not None):
        # 视频适配背景
        if back_size[0] > back_size[1]:
            new_height = 1080 * background_pic_rate
            new_width = new_height * video.size[0] / video.size[1]
        else:
            new_width = 1080 * background_pic_rate
            new_height = new_width * video.size[1] / video.size[0]
        video = video.resize((new_width, new_height))
        # 叠层
        video = CompositeVideoClip([background_clip, video, water_clip])
    elif background_pic is not None:
        if back_size[0] > back_size[1]:
            new_height = 1080 * background_pic_rate
            new_width = new_height * video.size[0] / video.size[1]
        else:
            new_width = 1080 * background_pic_rate
            new_height = new_width * video.size[1] / video.size[0]
        video = video.resize((new_width, new_height))
        # 叠层
        video = CompositeVideoClip([background_clip, video])

    elif logo is not None:
        video = CompositeVideoClip([video, water_clip])

    if save_path is not None:
        video.write_videofile(save_path + os.sep + name)
    else:
        video.write_videofile(os.path.dirname(sys.executable) + os.sep + name)

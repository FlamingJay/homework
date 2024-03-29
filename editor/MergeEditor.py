from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips, afx, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
import datetime
from editor.AutoEditor import AutoEditor
import os
import sys

class MergeEditor(AutoEditor):
    def __init__(self, background_pic=None, background_pic_rate=None, background_music=None, volume=None, is_covered_music=None, water_logo=None,
                 save_path=None):
        super(MergeEditor, self).__init__()
        self.background_pic = background_pic
        self.background_pic_rate = 1.0 if background_pic_rate is None else float(background_pic_rate)
        self.background_audio = background_music
        self.volume = 0 if volume is None else int(volume)
        self.original_autio_off = False if is_covered_music is None else is_covered_music
        self.water_logo = water_logo
        self.output_path = save_path

    
    def videos_edit(self, video_list):
        '''
        视频合集制作
        :param video_list: 要合成的单个视频列表
        :return:
        '''
        videos = []
        for item in video_list:
            videos.append(VideoFileClip(item))

        all_videos = concatenate_videoclips(videos)
        all_videos = all_videos.set_position('center')

        # 背景图
        if self.background_pic is not None:
            background_clip = ImageClip(self.background_pic)
            background_clip = background_clip.set_pos('center').set_duration(all_videos.duration)
            back_size = background_clip.size

        if self.water_logo is not None:
            water_clip = ImageClip(self.water_logo)
            water_clip = water_clip.set_pos('center').set_duration(all_videos.duration)

        if (self.background_pic is not None) and (self.water_logo is not None):
            # 视频适配背景
            if back_size[0] > back_size[1]:
                new_height = 1080 * self.background_pic_rate
                new_width = new_height * all_videos.size[0] / all_videos.size[1]
                background_clip = background_clip.resize((1920, 1080))
            else:
                new_width = 1080 * self.background_pic_rate
                new_height = new_width * all_videos.size[1] / all_videos.size[0]
                background_clip = background_clip.resize((1080, 1920))
            all_videos = all_videos.resize((new_width, new_height))
            all_videos = all_videos.set_position('center')
            # 叠层
            all_videos = CompositeVideoClip([background_clip, all_videos, water_clip])
        elif self.background_pic is not None:
            if back_size[0] > back_size[1]:
                new_height = 1080 * self.background_pic_rate
                new_width = new_height * all_videos.size[0] / all_videos.size[1]
                background_clip = background_clip.resize((1920, 1080))
            else:
                new_width = 1080 * self.background_pic_rate
                new_height = new_width * all_videos.size[1] / all_videos.size[0]
                background_clip = background_clip.resize((1080, 1920))
            all_videos = all_videos.resize((new_width, new_height))
            all_videos = all_videos.set_position('center')
            all_videos = CompositeVideoClip([background_clip, all_videos])
        elif self.water_logo is not None:
            all_videos = CompositeVideoClip([all_videos, water_clip])

        # 背景乐
        if self.background_audio is not None:
            # 要添加的音频
            audio_clip = AudioFileClip(self.background_audio)
            audio = afx.audio_loop(audio_clip, duration=all_videos.duration)
            audio = audio.volumex(int(self.volume) / 100)

            if self.original_autio_off:
                all_videos = all_videos.without_audio()
                all_videos = all_videos.set_audio(audio)
            else:
                # 原来的音频
                video_audio_clip = all_videos.audio
                all_videos = all_videos.set_audio(CompositeAudioClip([video_audio_clip, audio]))

        # 写入
        cur_time = datetime.date.today()
        if self.output_path is not None:
            save_path = self.output_path + os.sep + str(cur_time) + "_1.mp4"
            i = 0
            while os.path.exists(save_path):
                i += 1
                save_path = save_path[:-6] + "_" + str(i) + ".mp4"
            all_videos.write_videofile(save_path)
        else:
            all_videos.write_videofile(os.path.dirname(sys.executable) + os.sep + str(cur_time) + ".mp4")
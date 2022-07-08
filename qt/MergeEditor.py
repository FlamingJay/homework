from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips, afx, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
import datetime
from qt.AutoEditor import AutoEditor
import os
import sys

class MergeEditor(AutoEditor):
    def __init__(self, background_pic=None, background_music=None, volume=None, is_covered_music=None, water_logo=None,
                 save_path=None, time_cut_params=None, crop_params=None):
        super(MergeEditor, self).__init__()
        self.background_pic = background_pic
        self.background_audio = background_music
        self.volume = volume
        self.original_autio_off = is_covered_music
        self.water_logo = water_logo
        self.output_path = save_path
        self.time_cut_params = time_cut_params
        self.crop_params = crop_params
        
    def prepare_videos(self, video_path):
        pass
    
    def videos_edit(self, video_list):
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
                new_height = 1080 * 0.946
                new_width = new_height * all_videos.size[0] / all_videos.size[1]
                new_height = new_height
            else:
                new_width = 1080 * 0.946
                new_height = new_width * all_videos.size[1] / all_videos.size[0]
            all_videos = all_videos.resize((new_width, new_height))

            # 叠层
            all_videos = CompositeVideoClip([background_clip, all_videos, water_clip])
        elif self.background_pic is not None:
            if back_size[0] > back_size[1]:
                new_height = 1080 * 0.946
                new_width = new_height * all_videos.size[0] / all_videos.size[1]
            else:
                new_width = 1080 * 0.946
                new_height = new_width * all_videos.size[1] / all_videos.size[0]
            all_videos = all_videos.resize((new_width, new_height))

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
        # 加弹窗
        if self.output_path is not None:
            all_videos.write_videofile(self.output_path + "/" + str(cur_time) + ".mp4")
        else:
            all_videos.write_videofile(os.path.dirname(sys.executable) + "/" + str(cur_time) + ".mp4")
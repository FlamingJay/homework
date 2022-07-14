from editor.VideoProcess import single_process
from editor.AutoEditor import AutoEditor
import multiprocessing


class SingleEditor(AutoEditor):
    def __init__(self, background_pic=None, background_music=None, volume=None, is_covered_music=None, water_logo=None,
                 save_path=None, crop_x_start=0, crop_y_start=0, crop_x_end=0, crop_y_end=0, front_cut_dur=0, end_cut_dur=0):
        super(SingleEditor, self).__init__()
        self.background_pic = background_pic
        self.background_audio = background_music
        self.volume = volume
        self.original_autio_off = is_covered_music
        self.water_logo = water_logo
        self.output_path = save_path
        self.crop_x_start = crop_x_start
        self.crop_y_start = crop_y_start
        self.crop_x_end = crop_x_end
        self.crop_y_end = crop_y_end
        self.front_cut_dur = front_cut_dur
        self.end_cut_dur = end_cut_dur

    def videos_edit(self, video_list):
        '''
        :param video_list: 最终要进行处理的视频
        :return:
        '''
        videos = []
        names = []

        if video_list is None or len(video_list) < 1:
            return
        for file in video_list:
            videos.append(file)
            names.append(file.split("/")[-1])

        count = len(videos)
        muisic = [self.background_audio] * count
        pic = [self.background_pic] * count
        save_path = [self.output_path] * count
        crop_x_start = [self.crop_x_start] * count
        crop_y_start = [self.crop_y_start] * count
        crop_x_end = [self.crop_x_end] * count
        crop_y_end = [self.crop_y_end] * count
        water_logo = [self.water_logo] * count
        front_cut = [self.front_cut_dur] * count
        end_cut = [self.end_cut_dur] * count

        if self.volume is not None:
            volume = [int(self.volume)] * count
        else:
            volume = [0] * count

        audio_off = [self.original_autio_off] * count

        # 对每一个视频都做同样的操作
        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            pool.map(single_process,
                     zip(videos, names, muisic, volume, audio_off, pic, save_path, crop_x_start, crop_y_start,
                         crop_x_end, crop_y_end, water_logo, front_cut, end_cut))

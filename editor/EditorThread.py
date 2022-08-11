from PyQt5.QtCore import QThread, pyqtSignal

from ui.LoadingDialog import LoadingDialog
from editor.MergeEditor import MergeEditor
from editor.SingleEditor import SingleEditor


class EditorThread(QThread):
    _signal = pyqtSignal(int)

    def __init__(self, editor_type, source_videos_list, background_pic, background_pic_rate, background_music, volume, is_covered_music, water_logo, save_path, editor_params_dict):
        super(EditorThread, self).__init__()
        self.editor_type = editor_type
        self.source_videos_list = source_videos_list
        self.background_pic = background_pic
        self.background_pic_rate = background_pic_rate
        self.background_audio = background_music
        self.volume = volume
        self.original_autio_off = is_covered_music
        self.water_logo = water_logo
        self.output_path = save_path
        self.editor_params_dict = editor_params_dict

        self.editor = self.__create_editor__()

    def __create_editor__(self):
        if self.editor_type == "single":
            return SingleEditor(self.background_pic, self.background_pic_rate, self.background_audio, self.volume, self.original_autio_off, self.water_logo, self.output_path,
                                self.editor_params_dict["input_start_x"], self.editor_params_dict["input_start_y"],
                                self.editor_params_dict["input_end_x"], self.editor_params_dict["input_end_y"],
                                self.editor_params_dict["front_cut_dur"], self.editor_params_dict["end_cut_dur"])
        elif self.editor_type == "merge":
            return MergeEditor(self.background_pic, self.background_pic_rate, self.background_audio, self.volume, self.original_autio_off, self.water_logo, self.output_path)

    def __del__(self):
        self.wait()

    def run(self) -> None:
        if self.editor_type == "single":
            self.editor.videos_edit(self.source_videos_list)
        else:
            for videos in self.source_videos_list:
                self.editor.videos_edit(videos)

    def stop(self):
        self.terminate()
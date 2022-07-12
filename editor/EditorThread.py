from PyQt5.QtCore import QThread, pyqtSignal

from editor.MergeEditor import MergeEditor
from editor.SingleEditor import SingleEditor


class EditorThread(QThread):
    mask_video_index = []
    wait_to_cut = True

    _signal = pyqtSignal(list)

    def __init__(self, editor_type, source_videos_list, background_pic, background_music, volume, is_covered_music, water_logo, save_path, editor_params_dict):
        super(EditorThread, self).__init__()
        self.editor_type = editor_type
        self.source_videos_list = source_videos_list
        self.background_pic = background_pic
        self.background_audio = background_music
        self.volume = volume
        self.original_autio_off = is_covered_music
        self.water_logo = water_logo
        self.output_path = save_path
        self.editor_params_dict = editor_params_dict

        self.editor = self.__create_editor__()

    def __create_editor__(self):
        if self.editor_type == "single":
            return SingleEditor(self.background_pic, self.background_audio, self.volume, self.original_autio_off, self.water_logo, self.output_path,
                                self.editor_params_dict["time_cut_params"], self.editor_params_dict["crop_params"])
        elif self.editor_type == "merge":
            return MergeEditor(self.background_pic, self.background_audio, self.volume, self.original_autio_off, self.water_logo, self.output_path,
                                self.editor_params_dict["time_cut_params"], self.editor_params_dict["crop_params"])

    def __del__(self):
        self.wait()

    def run(self) -> None:
        # 处理
        self.editor.videos_edit(self.source_videos_list)
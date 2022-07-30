from PyQt5.QtCore import QThread, pyqtSignal
import os
import re
import time
from download.Translator import baiduAPI_translate


class TranslateThread(QThread):
    _translate_signal = pyqtSignal(int)

    def __init__(self, file_path):
        super(TranslateThread, self).__init__()
        self.file_path = file_path

    def __del__(self):
        self.wait()

    def run(self):
        if self.file_path == "":
            return

        file_path = self.file_path
        files = os.listdir(file_path)
        count = len(files)
        for i, file in enumerate(files):
            try:
                time.sleep(1)
                res = baiduAPI_translate(file[:-4].replace(" ", ""), "zh", "en")
                new_file = re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9\.\_ ]', '', res)
                new_file = new_file[:min(len(new_file), 100)]
                os.rename(file_path + os.sep + file, file_path + os.sep + new_file + ".mp4")
                self._translate_signal.emit(int((i+1) / count * 100))
            except Exception:
                print("error translate")
            finally:
                pass
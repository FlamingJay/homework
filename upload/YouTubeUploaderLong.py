#-*- coding: utf-8 -*-
from typing import DefaultDict, Optional
from selenium.webdriver.common.action_chains import ActionChains
import time
from collections import defaultdict
import json
import logging
from Constant import YOUTUBE_CONSTANT
from ChromeDriver import ChromeDriver
logging.basicConfig()


def load_metadata(metadata_json_path: Optional[str] = None) -> DefaultDict[str, str]:
    if metadata_json_path is None:
        return defaultdict(str)
    with open(metadata_json_path, encoding='utf-8') as metadata_json_file:
        return defaultdict(str, json.load(metadata_json_file))


class YouTubeUploaderLong:
    def __init__(self, root_path: str, account: str, video_path: str, metadata_json_path: Optional[str] = None, thumbnail_path: Optional[str] = None) -> None:
        self.account = account
        self.video_path = video_path
        self.thumbnail_path = thumbnail_path
        self.metadata_dict = load_metadata(metadata_json_path)
        current_working_dir = root_path
        self.browser = ChromeDriver(current_working_dir, current_working_dir)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def upload(self):
        try:
            self.logger.info("step 1: logging....")
            self.__login()
            self.logger.info("step 2: ready to upload....")
            self.__upload()
        except Exception as e:
            print(e)
            self.__quit()
            raise

    def __login(self):
        self.browser.driver.get(YOUTUBE_CONSTANT.YOUTUBE_URL)
        time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)
        if self.browser.has_cookies_for_current_website(self.account):
            self.browser.load_cookies(self.account)
            time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)
            self.browser.refresh()
        else:
            self.logger.info('Please sign in and then press enter')
            input()
            self.browser.get(YOUTUBE_CONSTANT.YOUTUBE_URL)
            time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)
            self.browser.save_cookies(self.account)

    def __quit(self):
        self.browser.quit()

    def __upload(self) -> (bool, Optional[str]):
        # 要上传视频的路径
        absolute_video_path = self.video_path

        # 打开相应的网页
        self.logger.info("step 3: open the YOUTUBE website....")
        self.browser.get(YOUTUBE_CONSTANT.YOUTUBE_UPLOAD_URL)
        time.sleep(YOUTUBE_CONSTANT.LOAD_TIME)

        # 上传视频
        self.logger.info("step 4: uploading the video....")
        self.browser.find_element_by_xpath(YOUTUBE_CONSTANT.INPUT_FILE_VIDEO)\
            .send_keys(absolute_video_path)

        self.logger.debug('Attached video {}'.format(self.video_path))
        time.sleep(YOUTUBE_CONSTANT.LONG_UPLOAD_TIME)

        # 填写title/desc
        self.logger.info("step 5: fill in the title and desc....")
        title = self.browser.find_element_by_id(YOUTUBE_CONSTANT.TEXTBOX)
        title.clear()
        self.browser.driver.implicitly_wait(10)
        ActionChains(self.browser.driver).move_to_element(title).click(title).send_keys(self.metadata_dict[self.account + '_title_long']).perform()
        time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)

        desc = self.browser.find_elements_by_id(YOUTUBE_CONSTANT.TEXTBOX)[1]
        desc.clear()
        self.browser.driver.implicitly_wait(10)
        ActionChains(self.browser.driver).move_to_element(desc).click(desc).send_keys(self.metadata_dict[self.account + '_description']).perform()

        self.browser.driver.execute_script("window.scrollTo(150, 900);")
        time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)

        # 儿童
        self.browser.find_elements_by_id(YOUTUBE_CONSTANT.NOT_MADE_FOR_KIDS_LABEL)[1].click()
        time.sleep(YOUTUBE_CONSTANT.LOAD_TIME)

        # 展开加入tag
        self.browser.driver.execute_script("window.scrollTo(250, 900);")
        self.browser.find_element_by_id(YOUTUBE_CONSTANT.TOOGLE_BUTN).click()
        tags = self.browser.find_elements_by_id(YOUTUBE_CONSTANT.TAGS_INPUT)[1]
        tags.clear()
        self.browser.driver.implicitly_wait(10)
        ActionChains(self.browser.driver).move_to_element(tags).click(tags).send_keys(self.metadata_dict[self.account + '_tag']).perform()
        time.sleep(YOUTUBE_CONSTANT.LONG_WAIT_TIME)

        # # 允许审查
        self.browser.find_element_by_id(YOUTUBE_CONSTANT.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} one'.format(YOUTUBE_CONSTANT.NEXT_BUTTON))
        time.sleep(YOUTUBE_CONSTANT.LONG_WAIT_TIME)

        self.browser.find_element_by_id(YOUTUBE_CONSTANT.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} two'.format(YOUTUBE_CONSTANT.NEXT_BUTTON))
        time.sleep(YOUTUBE_CONSTANT.LONG_WAIT_TIME)

        self.browser.find_element_by_id(YOUTUBE_CONSTANT.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} three'.format(YOUTUBE_CONSTANT.NEXT_BUTTON))
        time.sleep(YOUTUBE_CONSTANT.LONG_WAIT_TIME)

        # 公开发布
        self.browser.find_element_by_name(YOUTUBE_CONSTANT.PUBLIC_BUTTON).click()
        self.logger.debug('Made the video {}'.format(YOUTUBE_CONSTANT.PUBLIC_BUTTON))
        time.sleep(YOUTUBE_CONSTANT.LOAD_TIME)

        done_button = self.browser.find_element_by_id(YOUTUBE_CONSTANT.DONE_BUTTON)
        done_button.click()
        self.logger.info("step 8: finished....")
        time.sleep(YOUTUBE_CONSTANT.LONG_WAIT_TIME)

        self.browser.quit()

    def __write_field(self, xpath, dic):
        self.browser.find_element_by_xpath(xpath).click()
        self.browser.find_element_by_xpath(xpath).clear()
        time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)

        self.browser.find_element_by_xpath(xpath).send_keys(dic['caption'])
        time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)


if __name__ == "__main__":
    uploader = YouTubeUploaderLong("jie", "new bag.mp4", "conf.json", None)
    uploader.upload()

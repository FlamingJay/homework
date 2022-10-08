#-*- coding: utf-8 -*-
import os.path
from typing import DefaultDict, Optional
from selenium.webdriver.common.action_chains import ActionChains
import time
from collections import defaultdict
import json
import logging
from Constant import YOUTUBE_CONSTANT
from HubChromeDriver import HubChromeDriver
from ChromeDriver import ChromeDriver
logging.basicConfig()


class YouTubeUploaderShort:
    def __init__(self, pkl_path: str, account: str, video_path: str, title: str, caption: str, description: str, tags: str, title_tags: str, use_file_title:str, finger_web:str) -> None:
        self.account = account
        self.video_path = video_path
        self.title = title
        self.caption = caption
        self.description = description
        self.tags = tags
        self.title_tags = title_tags
        self.use_file_title = use_file_title == "true"
        current_working_dir = pkl_path
        if finger_web == "":
            self.browser = ChromeDriver(current_working_dir, current_working_dir)
        else:
            self.browser = HubChromeDriver(current_working_dir, current_working_dir, finger_web)
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
        file_name = self.video_path.split("\\")[-1][:-4]

        # 打开相应的网页
        self.logger.info("step 3: open the YOUTUBE website....")
        self.browser.get(YOUTUBE_CONSTANT.YOUTUBE_UPLOAD_URL)
        time.sleep(YOUTUBE_CONSTANT.LOAD_TIME)

        # 上传视频
        self.logger.info("step 4: uploading the video....")
        self.browser.find_element_by_xpath(YOUTUBE_CONSTANT.INPUT_FILE_VIDEO)\
            .send_keys(absolute_video_path)
        self.browser.driver.implicitly_wait(15)

        self.logger.debug('Attached video {}'.format(self.video_path))
        time.sleep(YOUTUBE_CONSTANT.SHORT_WAIT_TIME)
        time.sleep(YOUTUBE_CONSTANT.SHORT_WAIT_TIME)

        # 填写标题+title_tag、描述
        self.logger.info("step 5: fill in the title and desc....")
        title_ele = self.browser.find_element_by_id(YOUTUBE_CONSTANT.TEXTBOX)
        if self.use_file_title:
            upload_title = "  ".join([file_name, self.title_tags])
            ActionChains(self.browser.driver).move_to_element(title_ele).click(title_ele)
            title_ele.clear()
            self.browser.driver.implicitly_wait(5)
            ActionChains(self.browser.driver).move_to_element(title_ele).click(title_ele).send_keys(upload_title[:min(len(upload_title), 95)]).perform()
            time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)
        else:
            upload_title = "  ".join([self.title, self.title_tags])
            ActionChains(self.browser.driver).move_to_element(title_ele).click(title_ele)
            title_ele.clear()
            self.browser.driver.implicitly_wait(5)
            ActionChains(self.browser.driver).move_to_element(title_ele).click(title_ele).send_keys(upload_title[:min(len(upload_title), 95)]).perform()
            time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)

        desc_ele = self.browser.find_elements_by_id(YOUTUBE_CONSTANT.TEXTBOX)[1]
        ActionChains(self.browser.driver).move_to_element(desc_ele).click(desc_ele)
        self.browser.driver.implicitly_wait(5)
        ActionChains(self.browser.driver).move_to_element(desc_ele).click(desc_ele).send_keys(self.description).perform()
        desc_ele.clear()
        self.browser.driver.implicitly_wait(5)

        # 选择缩略图
        pic_path = absolute_video_path.replace(r".mp4", r".jpg")
        if os.path.exists(pic_path):
            self.logger.info("step 5: fill in the cover of video....")
            self.browser.find_element_by_id(YOUTUBE_CONSTANT.PICTURE_BUTTON).send_keys(pic_path)
            self.browser.driver.implicitly_wait(5)

        self.browser.driver.execute_script("window.scrollTo(150, 900);")
        time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)

        # 儿童
        self.browser.find_elements_by_id(YOUTUBE_CONSTANT.NOT_MADE_FOR_KIDS_LABEL)[1].click()
        time.sleep(YOUTUBE_CONSTANT.CONFIRM_TIME)

        # 展开加入tag
        self.browser.driver.execute_script("window.scrollTo(250, 900);")
        self.browser.find_element_by_id(YOUTUBE_CONSTANT.TOOGLE_BUTN).click()
        tags = self.browser.find_elements_by_id(YOUTUBE_CONSTANT.TAGS_INPUT)[1]
        tags.clear()
        self.browser.driver.implicitly_wait(10)
        ActionChains(self.browser.driver).move_to_element(tags).click(tags).send_keys(self.tags).perform()
        time.sleep(YOUTUBE_CONSTANT.CONFIRM_TIME)

        # # 允许审查
        self.browser.find_element_by_id(YOUTUBE_CONSTANT.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} one'.format(YOUTUBE_CONSTANT.NEXT_BUTTON))
        time.sleep(YOUTUBE_CONSTANT.SHORT_WAIT_TIME)

        self.browser.find_element_by_id(YOUTUBE_CONSTANT.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} two'.format(YOUTUBE_CONSTANT.NEXT_BUTTON))
        time.sleep(YOUTUBE_CONSTANT.SHORT_WAIT_TIME)

        self.browser.find_element_by_id(YOUTUBE_CONSTANT.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} three'.format(YOUTUBE_CONSTANT.NEXT_BUTTON))
        time.sleep(YOUTUBE_CONSTANT.SHORT_WAIT_TIME)

        # 公开发布
        self.browser.find_element_by_name(YOUTUBE_CONSTANT.PUBLIC_BUTTON).click()
        self.logger.debug('Made the video {}'.format(YOUTUBE_CONSTANT.PUBLIC_BUTTON))
        time.sleep(YOUTUBE_CONSTANT.LOAD_TIME)

        done_button = self.browser.find_element_by_id(YOUTUBE_CONSTANT.DONE_BUTTON)
        done_button.click()
        self.logger.info("step 8: finished....")
        time.sleep(YOUTUBE_CONSTANT.SHORT_WAIT_TIME)

        self.browser.quit()


    def __write_field(self, xpath, dic):
        self.browser.find_element_by_xpath(xpath).click()
        self.browser.find_element_by_xpath(xpath).clear()
        time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)

        self.browser.find_element_by_xpath(xpath).send_keys(dic['caption'])
        time.sleep(YOUTUBE_CONSTANT.USER_WAITING_TIME)


if __name__ == "__main__":
    uploader = YouTubeUploaderShort("jie", "new bag.mp4", "conf.json", None)
    uploader.upload()

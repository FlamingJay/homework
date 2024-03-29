#-*- coding: utf-8 -*-
import json
import os
import argparse
from YouTubeUploaderShort import YouTubeUploaderShort
from YouTubeUploaderLong import YouTubeUploaderLong
from TikTokUploader import TiktokUploader


def pick_video(hist_path, target_path):
    '''
    选择一个未上传过的视频进行上传
    :param path:
    :return:
    '''
    history = []
    if not os.path.exists(hist_path):
        file = open(hist_path, "w", encoding="utf-8")
        file.close()
    with open(hist_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            history.append(line.strip())

    # 随机上传
    files = get_file_list(target_path)
    target = ""
    for file in files:
        print(file)
        if file not in history:
            target = file
            break

    return target


def add_hist(path, name):
    '''
    将当前上传的视频标记为已上传
    :param path:
    :param name:
    :return:
    '''
    with open(path, 'a', encoding="utf-8") as f:
        f.write(name + "\n")


def get_file_list(file_path):
    '''
    按照文件最后修改时间进行升序排序
    '''
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        dir_list = sorted(filter(lambda item: 'mp4' in item, dir_list), key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        return dir_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--root", help='account', required=True)

    parser.add_argument("--account", help='account', required=True)

    parser.add_argument("--web", help='web', required=True)

    parser.add_argument("--meta", help='meta', required=True)

    parser.add_argument("--video_path", help='Path to the video file', required=True)

    parser.add_argument("--video_type", help="video_type", required=True)

    parser.add_argument("--use_file_title", help="use_file_title", required=True)

    parser.add_argument("--finger_web", help="use_file_title", required=True)

    args = parser.parse_args()

    # 解析参数
    accounts = dict()
    root = os.path.abspath(os.path.join(args.root, ".."))
    with open(root + os.sep + "resource" + os.sep + args.meta) as f:
        accounts = json.load(f)

    title = accounts[args.account]["title"]
    caption = accounts[args.account]["caption"]
    description = accounts[args.account]["description"]
    tags = accounts[args.account]["tags"]
    title_tags = accounts[args.account]["title_tags"]
    resources = root + os.sep + "resource"

    if args.web == "youtube":
        hist_path = resources + os.sep + "_".join([args.web, args.account, args.video_type]) + ".txt"
        target = pick_video(hist_path, args.video_path)
        if target is not "":
            if args.video_type == "short":
                print("short")
                add_hist(hist_path, target)
                uploader = YouTubeUploaderShort(pkl_path=resources,
                                            account=args.account,
                                            video_path=args.video_path + os.sep + target,
                                            title=title,
                                            caption=caption,
                                            description=description,
                                            tags=tags,
                                            title_tags=title_tags,
                                            use_file_title=args.use_file_title,
                                            finger_web=args.finger_web
                                           )
                uploader.upload()
            elif args.video_type == "long":
                print("long")
                add_hist(hist_path, target)
                uploader = YouTubeUploaderLong(pkl_path=resources,
                                               account=args.account,
                                               video_path=args.video_path + os.sep + target,
                                               title=title,
                                               caption=caption,
                                               description=description,
                                               tags=tags,
                                               title_tags=title_tags,
                                               use_file_title=args.use_file_title,
                                               finger_web=args.finger_web
                                           )
                print("ready to upload")
                uploader.upload()
    elif args.web == "tiktok":
        hist_path = resources + os.sep + "tiktok_" + args.account + ".txt"
        target = pick_video(hist_path, args.video_path)

        if target is not "":
            print("tiktok")
            add_hist(hist_path, target)
            uploader = TiktokUploader(pkl_path=resources,
                                      account=args.account,
                                      video_path=args.video_path + os.sep + target,
                                      title=title,
                                      caption=caption,
                                      description=description,
                                      tags=tags,
                                      title_tags=title_tags,
                                      use_file_title=args.use_file_title,
                                      finger_web=args.finger_web
                                      )
            uploader.upload()

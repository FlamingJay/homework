#-*- coding: utf-8 -*-
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
    print(target_path)
    history = []
    if not os.path.exists(hist_path):
        file = open(hist_path, "w", encoding="utf-8")
        file.close()
    with open(hist_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            history.append(line.strip())

    # 随机上传
    files = os.listdir(target_path)
    target = ""
    for file in files:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", help='Path to the code file', required=True)

    parser.add_argument("--account", help='account', required=True)

    parser.add_argument("--web", help='web', required=True)

    parser.add_argument("--title", help='title', required=False)

    parser.add_argument("--caption", help="caption", required=False)

    parser.add_argument("--description", help="description", required=False)

    parser.add_argument("--tags", help='tags', required=False)

    parser.add_argument("--title_tags", help='tags', required=False)

    parser.add_argument("--video_path", help='Path to the video file', required=True)

    parser.add_argument("--video_type", help="video_type", required=True)

    parser.add_argument("--use_file_title", help="use_file_title", required=True)

    args = parser.parse_args()
    if args.web == "youtube":
        hist_path = args.root + "\\youtube_" + args.account + ".txt"
        target = pick_video(hist_path, args.video_path)
        if target is not "":
            if args.video_type == "short":
                print("short")
                uploader = YouTubeUploaderShort(root_path=args.root,
                                            account=args.account,
                                            video_path=args.video_path + "/" + target,
                                            title=args.title,
                                            caption = args.caption,
                                            description=args.description,
                                            tags=args.tags,
                                            title_tags=args.title_tags,
                                            use_file_title=args.use_file_title
                                           )
                uploader.upload()
            elif args.video_type == "long":
                print("long")
                uploader = YouTubeUploaderLong(root_path=args.root,
                                                account=args.account,
                                                video_path=args.video_path + "/" + target,
                                                title=args.title,
                                                caption=args.caption,
                                                description=args.description,
                                                tags=args.tags,
                                                title_tags=args.title_tags,
                                                use_file_title=args.use_file_title
                                           )
                print("ready to upload")
                uploader.upload()
        add_hist(hist_path, target)
    elif args.web == "tiktok":
        hist_path = args.root + "\\tiktok_" + args.account + ".txt"
        target = pick_video(hist_path, args.video_path)

        if target is not "":
            uploader = TiktokUploader(root_path=args.root,
                                      account=args.account,
                                      video_path=args.video_path + "/" + target,
                                      title=args.title,
                                      caption=args.caption,
                                      description=args.description,
                                      tags=args.tags,
                                      title_tags=args.title_tags,
                                      use_file_title=args.use_file_title
                                      )
            uploader.upload()
        add_hist(hist_path, target)
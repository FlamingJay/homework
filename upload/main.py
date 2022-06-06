import os
import argparse
from YouTubeUploader import YouTubeUploader
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
    parser.add_argument("--root",
                        help='Path to the video file',
                        required=True)

    parser.add_argument("--web",
                        help='Path to the video file',
                        required=True)

    parser.add_argument("--account",
                        help='Path to the video file',
                        required=True)

    parser.add_argument("--video_path",
                        help='Path to the video file',
                        required=True
                        )

    parser.add_argument("--hist_path",
                        help='Path to the video file',
                        required=True
                        )

    args = parser.parse_args()

    if args.web == "youtube":
        target = pick_video(args.root + args.hist_path, args.video_path)
        print(target)
        if target is not "":
            uploader = YouTubeUploader(args.account, args.video_path + "/" + target, args.root + "\conf.json", None)
            uploader.upload()
        add_hist(args.root + args.hist_path, target)
    elif args.web == "tiktok":
        target = pick_video(args.root + args.hist_path, args.video_path)
        if target is not "":
            uploader = TiktokUploader(args.account, args.video_path + "/" + target, args.root + "\conf.json", None)
            uploader.upload()
        add_hist(args.root + args.hist_path, target)
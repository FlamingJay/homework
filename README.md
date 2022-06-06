# homework
跟杜总的小作业

1.自动化下载

    使用的是tkinker。打包exe的时候，需要加载gif，所以执行的命令为：
    1、pyinstaller -F -w -i .\pic.ico .\shortVideo.py
    2、修改spec文件，将资源文件加载到其中，pathex改为文件所在路径，datas改为gif的相对路径
    3、pyinstaller shortVideo.spec

2.自动化剪辑

    使用的是pyqt

3.自动化上传：

    使用的浏览器驱动是undetected_chromedriver，可以跳过tiktok的机器人检查
    使用的浏览器是91，版本：Google_Chrome_(64bit)_v91.0.4472.77
这是一个用python写的一个简易podcast的rss生成系统。

该系统提供一个命令行程序，比如 ypd add https://www.youtube.com/watch?v=rXa3pW2sarg 
运行以上命令后自动从给的YouTube地址下载音频文件并且将视频信息加到podcast的rss xml中。
下载后的原始数据保存在podcast.json中，rss保存在feed.xml中。

ypd.py是命令行程序的代码

并且提供一个简易的web服务来访问这个rss, webapp.py是web服务的代码，
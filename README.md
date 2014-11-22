## Hcrab

### Introduction

**Hcrab** is a YouTube video offline download web service.

Demo site: <http://d.jaylab.org>

### Installation
On a Ubuntu system

1. sudo apt-get install python-pip git (Install nginx if you want Hcrab to be hosted by nginx)
2. Download the source code: git clone https://xiaojay@bitbucket.org/xiaojay/jaylab-download.git
3. Suppose if you download it into /home/jay/websites/jaylab-download, then
cd /home/jay/websites/jaylab-download
4. sudo pip install -r requirements.pip (You may use virtualenv here) 
5. Generate the database: mkdir jaylab/db; ./manage.py syncdb -all(You will be promoted for a admin username/password); ./manage.py migrate --fake
6. Edit the config file: vim jaylab/app_settings.py, then change HOST and SERVER_VIDEO_DIR(where the downloaded video will be stored).

### Testing
7. Add the code directory to python sys.path:
sudo cp config/jay.pth /usr/lib/python2.7/dist-packages/ 
8. ./manage.py runserver 0.0.0.0:8000; Open http://your-host:8000 with your browser, then add an YouTube link.
9. run python jaylab/hcrab/download.py to test the video download.

### Production deployment
10. ./manage.py collectstatic
11. Edit the nginx config file: vim config/hcrab (you should change /home/jay/websites/download.jaylab.org/ to your path)
12. sudo cp config/hcrab /etc/nginx/site-available; sudo ln -s /etc/nginx/site-avaiable/hcrab /etc/nginx/site-enabled/;sudo service nginx reload
13. Use gunicorn as wsgi server: gunicorn django -D -b 127.0.0.1:8000 jaylab/settings.py
14. Add download.py to crontab, run every minute.

### Credit
You can use hcrab to do anything you want, but I would appreciate it if you keep the page footer.


**Below is a Chinese version of README**


## 寄居蟹Hcrab

### 介绍

**寄居蟹Hcrab**，是一个离线下载youtube视频的web服务。

Demo site: <http://d.jaylab.org>

### 安装
ubuntu系统

1. sudo apt-get install nginx python-pip git
2. 下载代码： git clone https://xiaojay@bitbucket.org/xiaojay/jaylab-download.git
3. 假设你下载到 /home/jay/websites/jaylab-download, 
cd /home/jay/websites/jaylab-download.
4. sudo pip install -r requirements.pip (你也可以使用virtualenv)
5. 生成数据库： mkdir jaylab/db; ./manage.py syncdb -all(会出现要求你输入后台管理的用户名和密码)；./manage.py migrate --fake
6. 更改配置文件: vim jaylab/app_settings.py; 更改其中的HOST 和SERVER_VIDEO_DIR（这个是你存放下载的video的目录）选项。

###### 测试
7. 将代码目录添加到python sys.path:
修改config/jay.pth 的中的目录为你的代码的目录；
sudo cp config/jay.pth /usr/lib/python2.7/dist-packages/ 
8. ./manage.py runserver 0.0.0.0:8000; 用浏览器打开http://your-host:8000（主界面）, 添加一个youtube链接.   
9. 测试下载 , python jaylab/hcrab/download.py

###### 实际生产环境下网站
10. ./manage.py collectstatic
11. 修改nginx设置文件. vim config/hcrab (主要修改/home/jay/websites/download.jaylab.org/为你的目录)
12. sudo cp config/hcrab /etc/nginx/site-avaiable;sudo ln -s /etc/nginx/site-avaiable/hcrab /etc/nginx/site-enabled/;sudo service nginx reload
13. 用gunicorn做wsgi server: gunicorn_django -D -b 127.0.0.1:8000 jaylab/settings.py
14. 把download.py 放到crontab，一分钟执行一次。

### 授权
你可以用hcrab的代码做任何事；不过，我会感谢你，如果你保留主页的footer ：） 

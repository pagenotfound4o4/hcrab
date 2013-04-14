## 寄居蟹Hcrab

### 介绍

**寄居蟹Hcrab**，是一个离线下载youtube视频的web服务。

### 安装
ubuntu系统

1. sudo apt-get install nginx python-pip git
2. 下载代码： git clone https://xiaojay@bitbucket.org/xiaojay/jaylab-download.it
3. 假设你下载到 /home/jay/websites/jaylab-download, 
   1. cd /home/jay/websites/jaylab-download
   2. sudo pip install -r requirements.pip
   3. mkdir jaylab/db; ./manage.py syncdb -all(会出现要求你输入后台管理的用户名和密码)；./manage.py migrate --fake
   4. 更改配置文件: vim jaylab/app_settings.py; 更改其中的HOST 和SERVER_VIDEO_DIR（这个是你存放下载的video的目录）选项。
   5. 测试： ./manage.py runserver 0.0.0.0:8000; 用浏览器打开http://your-host:8000（主界面）, 添加一个youtube链接。
   6. 测试下载 , python jaylab/hcrab/download.py
4. 测试成功后，设置实际运行环境下的网站。
   1. ./manage.py collectstatic
   2. 修改nginx设置文件. vim config/hcrab (主要修改/home/jay/websites/download.jaylab.org/为你的目录)
   3. sudo cp config/hcrab /etc/nginx/site-avaiable;ln -s /etc/nginx/site-avaiable/hcrab /etc/nginx/site-enabled/;sudo service nginx reload
   4. 用gunicorn做wsgi server: gunicorn -D -b 127.0.0.1:8000 jaylab/settings.py
   5、把download.py 放到crontab，一分钟执行一次。

### 授权
你可以用hcrab的代码做任何事；不过，我会感谢你，如果你保留主页的footer ：） 
>希望能够在技术上多多交流哇！
>
>个人博客：https://blog.csdn.net/weixin_35757704

# 概述
这是一个舆情监测系统，通过定时爬取百度新闻的新闻内容，然后提取出新闻文本的主题词与情感，保存下来以便日后研究。

>在未经修改的情况下，本系统只能运行在Linux操作系统上，详情请参考“代码逻辑”部分。

# 应用场景
作为一个采集数据与简单分析的系统，主要面向研究人员，为相关研究提供数据支持。
> 由于百度新闻会隔一段时间清理新闻，因此建议本系统一直部署在服务器端。

# 项目部署方法
1. 首先确保你的服务器已经安装 nginx，mysql服务端与客户端，gcc，与python3.4以上版本，以上依赖使用以下代码进行安装(以ubuntu为例，sentos请使用yum install安装)：
   
   ```bash
    sudo apt-get install nginx # nginx
    sudo apt-get install gcc # gcc
    sudo apt-get install python3-pip # python3 pip
    sudo apt-get install mysql-server # mysql server
    sudo apt-get install libmysqlclient-dev # mysql client
    ```
2. 建议先将所有文件clone到End这个文件夹下，然后将 End/ 文件夹放置在 /srv 目录下，千万不要放在 /root 下！
    ```bash
    mv End/ /srv/
    cd /srv/End/
    ```
3. 安装python3依赖包
   
   在 End/ 文件夹下有一个文件requirements.txt，它包含了这个项目使用的所有依赖包，使用pip工具来安装依赖包。   
    ```bash
    pip3 install -r requirements.txt # 确保pip3对应的python版本高于3.4
    pip3 install uwsgi # 并发访问依赖 uwsgi
    ```
    >请根据项目需要配置虚拟环境
4. 配置mysql
    ```sql
    mysql -u root -p
    ```
    在mysql命令行中执行以下代码，创建用户与项目数据库，并赋予用户权限。
    ```sql
    CREATE DATABASE `数据库名` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
    CREATE user '用户名'@'localhost' identified BY '密码';
    GRANT all privileges ON 数据库名.* TO 用户名@localhost identified BY '密码';
    flush privileges;
    exit;
    ```
5. 配置django
    ```bash
    cd Mainweb/
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py collectstatic
    ```
    然后创建一个系统管理员
    ```bash
    python3 manage.py createsuperuser
    # 依次输入用户名，邮箱，密码，确认密码
    ```
6. 配置nginx与uwsgi
   
   nginx配置文件是 End/conf/uc_nginx.conf，uwsgi的配置文件是 End/conf/uwsgi.ini
   >如果个性化需要，请修改配置文件
    ```bash
    # nginx
    # 请先修改 uc_nginx.conf 的server_name项中的ip地址，改为当前服务器的ip地址
    cp /srv/End/conf/uc_nginx.conf /etc/nginx/conf.d
    serviec nginx restart
    # uwsgi
    uwsgi -i uwsgi.ini &
    ```
    配置完成后，先关闭防火墙，尝试访问一下网站：
    ```bash
    # 暂时关闭防火墙
    sudo ufw disable 
    ```
    **如果访问当前服务器ip或域名成功，则说明以上配置正确，** 如果出现任何报错，请在issue上提问，或是查阅相关资料，good luck，这个过程往往是煎熬的......

7. 配置防火墙
    >如果使用阿里云服务器，由于阿里云额外有一层保护，所以请在阿里云服务器控制台打开80，443端口，而无需执行下面的代码。
   ```bash
    sudo ufw allow 22 # ssh
    sudo ufw allow 80 # http
    sudo ufw allow 443 # https
    sudo ufw enable
   ```
    配置完服务器后django的配置就结束了。

8. 配置爬虫周期性任务
    >如果项目目录不是 /srv ，请仔细修改 End/Mainscrapy/execute_xinwen.sh 的目录配置代码，如果有问题，请查看“技术详解博客”板块

    在命令行输入代码：
    ```bash
    #配置linux定时任务
    crontab -e
    ```
    在打开的文本最后一行添加下面的一行：
    ```bash
    */30 * * * * /bin/bash /srv/End/Mainscrapy/execute_xinwen.sh >> /srv/End/Mainscrapy/scrapy_log.txt
    ```
    Scrapy日志会打印在 /srv/End/Mainscrapy/scrapy_log.txt 中，如果日志打印正常，则说明系统爬虫配置完成。

9.  （可选）配置邮箱提醒
    
    当输入的一个主题第一次爬取完成后，系统可以进行邮件提醒，虽然我感觉用处不大，不过这是很简单的功能，捎带着就搞定了。
    ```bash
    #首先配置 End/Mainweb/Mainweb/settings.py 中邮件发送那一块，然后执行：
    python3 /srv/End/Mainweb/manage.py crontab add
    ```
# 代码逻辑
*本系统衍生出一篇会议论文，当论文收录后对这部分进行更加详细的更新。*

>技术上：系统的爬虫模块采用Scrapy框架，后端采用Django框架，配合前端框架，构造了一个“舆情监测系统”。

>建模上：系统主要使用自然语言处理领域方法，使用TF-IDF提取主题词，并通过2019年4月更新的维基百科中文语料库训练了一个word2vec模型，提供了一个非常有帮助的辅助模块。

下面是一些主要的文件：

+ Mainscrapy：*Scrapy爬虫框架代码*
    + execute_xinwen.sh：*Linux定时执行爬虫的脚本*
    + Mainscrapy：*爬虫代码*
      - xinwen_main.py： *定时爬取百度新闻的爬虫启动代码*
      - baidu_main.py：*爬取百度百科的爬虫启动代码*
      - <span>middlewares.py</span>：*爬虫伪装请求头*

+ Mainweb: *Django框架代码*
  + apps
    + background_ms：*处理系统前端操作对应的后端*
    + scrapy_app：*连接Scrapy框架*
    + user：*用户与用户组管理*
  + extra_apps：*模型训练相关代码*
  + templates：*前端网页文件*
  + static：*css，js文件*

# 技术详解博客
**Scrapy爬虫：**

>Scrapy周期性爬取（解决Unknown command: crawl报错）：https://blog.csdn.net/weixin_35757704/article/details/90204323

>Linux定时任务配置说明：https://blog.csdn.net/weixin_35757704/article/details/89227896#4.%E6%9B%B4%E5%8A%A0%E5%A4%8D%E6%9D%82%E7%9A%84%E9%85%8D%E7%BD%AE

>Scrapy 一些常用方法总结(调试,定时与测试):https://blog.csdn.net/weixin_35757704/article/details/86348587

**前端网页：**

>HTML5基础笔记:https://blog.csdn.net/weixin_35757704/article/details/52088865

>前端网页制作-javaScripe 笔记:https://blog.csdn.net/weixin_35757704/article/details/52130571

**后端Django框架：**

>django-crontab 快速配置,高效执行django的周期性任务:https://blog.csdn.net/weixin_35757704/article/details/89227896

>Nginx 502报错(django+nginx,而非php-fmp):https://blog.csdn.net/weixin_35757704/article/details/79984576

>scarpy 整合 djangoitem，摆脱保存数据时SQL报错的困扰:https://blog.csdn.net/weixin_35757704/article/details/78922114

>Django账号绑定邮箱时发送链接:https://blog.csdn.net/weixin_35757704/article/details/70194384

**自然语言处理模型训练：**

>数据分析（专栏）：https://blog.csdn.net/weixin_35757704/column/info/38577

>自然语言处理-LDA建模代码:https://blog.csdn.net/weixin_35757704/article/details/91443880

>TF-IDF 提取文本关键词:https://blog.csdn.net/weixin_35757704/article/details/87968553


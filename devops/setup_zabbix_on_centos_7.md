# CentOS 7搭建Zabbix服务器

## STEP 1: 安装MariaDB 10.2

### 添加MariaDB yum源

> vi /etc/yum.repo.d/MariaDB.repo

```markdown
[mariadb]
name = MariaDB
baseurl = http://mirrors.aliyun.com/mariadb/yum/10.2/centos7-amd64
gpgkey=http://mirrors.aliyun.com/mariadb/yum/RPM-GPG-KEY-MariaDB
gpgcheck=1
```
> yum makecache fast

### 安装mariadb
> yum install MariaDB-client MariaDB-server

### 安装过程中解决mariadb-libs-1:5.5.52-1.el7.x86_64冲突后，再次运行上面命令
> rpm -e  mariadb-libs-1:5.5.52-1.el7.x86_64 --nodeps

### 启动mariadb
> systemctl start mariadb
> systemctl enable  mariadb

## STEP 2: 安装Zabbix 3.2
##### [参考官方文档](https://www.zabbix.com/documentation/3.2/manual/installation/install_from_packages/server_installation_with_mysql)

### Installing repository configuration package

> rpm -ivh http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm

### Install Zabbix server and web frontend installation with MySQL database

> yum install zabbix-server-mysql zabbix-web-mysql

## STEP 3: Creating initial database
```markdown
shell> mysql -uroot -p<root_password>
mysql> create database zabbix character set utf8 collate utf8_bin;
mysql> grant all privileges on zabbix.* to zabbix@localhost identified by '<password>';
mysql> quit;
```
### Now import initial schema and data. Make sure to insert correct version for 3.2.*. You will be prompted to enter your newly created password.
> zcat /usr/share/doc/zabbix-server-mysql-3.2.*/create.sql.gz | mysql -uzabbix -p zabbix
#### In order to check the version you have in your package, use the following command:
> rpm -q zabbix-server-mysql
### Database configuration for Zabbix server
### Edit server host, name, user and password in zabbix_server.conf as follows, where DBPassword is the password you've set creating initial database:
> vi /etc/zabbix/zabbix_server.conf
```markdown
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=<password>
````
### Starting Zabbix server process
> systemctl start zabbix-server
> systemctl enable zabbix-server

### PHP configuration for Zabbix frontend
#### Apache configuration file for Zabbix frontend is located in /etc/httpd/conf.d/zabbix.conf. Some PHP settings are already configured. But it's necessary to #### uncomment the “date.timezone” setting and set the right timezone for you.

```markdown
php_value max_execution_time 300
php_value memory_limit 128M
php_value post_max_size 16M
php_value upload_max_filesize 2M
php_value max_input_time 300
php_value always_populate_raw_post_data -1
# php_value date.timezone Europe/Riga
```

> 修改注释行
> php_value date.timezone Asia/Shanghai

> 检查并设置timezone
> date
> timedatectl set-timezone Asia/Shanghai

### 开放80端口
> firewall-cmd --add-port=80/tcp --permanent
> firewall-cmd --reload

### 启动httpd
> systemctl start httpd

## STEP 4：Installing frontend 
### In your browser, open Zabbix URL: http://<server_ip_or_name>/zabbix
### You should see the first screen of the frontend installation wizard.
### 下面的步骤比较简单，基本一路下一步。就可以用默认账户Admin/zabbix登录了

### Setup Nginx for download server with basic authentication

#### Install nginx
> yum install -y nginx

#### Configure 
> vi /etc/nginx/nginx.conf

```markdown
    listen       8088 default_server;
    listen       [::]:8088 default_server;
```

```markdown
   location /download {
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        auth_basic "please log on...";
        auth_basic_user_file /usr/share/nginx/passwd;
    }
```

#### Configure firewall
> firewall-cmd --add-port=*8088*/tcp --permanent 


> firewall-cmd --reload

#### Add user
> htpasswd -c /usr/share/nginx/passwd andy

#### Create download directory
> mkdir /usr/share/nginx/html/download

#### Put your file to /usr/share/nginx/html/download

#### Start nginx service and make it start on boot
> systemctl start nginx

> systemctl enable nginx
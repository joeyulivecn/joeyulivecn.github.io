### Setup nginx and keepalived

#### Environment
* CentOS 7.3
* nginx version: 1.12.2
* keepalived version: v1.3.9

* Virtual IP: 192.168.100.40
* Load Balance 1: 
	* OS: CentOS 7.3
	* IP: 192.168.100.28
	* nginx
	* keepalived
* Load Balance 2:
	* CentOS 7.3
	* IP: 192.168.100.29
	* nginx
	* keepalived
* Backend Web Server 1: 
	* CentOS 7.3
	* IP: 192.168.100.30
	* nginx
* Backend Web Server 2: 
	* CentOS 7.3
	* IP: 192.168.100.32
	* nginx

https://github.com/joeyulivecn/joeyulivecn.github.io/raw/master/images/nginx_and_keepalived.png

#### Setup load balance with nginx (192.168.100.28, 192.168.100.29)
> yum install nginx

> vi /etc/nginx/nginx.conf
```markdown
    upstream webservers {
        server 192.168.100.30:80 weight=1;
        server 192.168.100.32:80 weight=1;
    }

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
            proxy_pass http://webservers;
            proxy_set_header X-Real-IP $remote_addr;
        }
```
> nginx -t

> nginx

> firewall-cmd --add-port=80/tcp --permanent

> firewall-cmd --reload

#### Setup backend web servers(192.168.100.30, 192.168.100.32)
> yum install nginx

> vi /usr/share/nginx/html/index.html

> add ip address of current host to <body>

> firewall-cmd --add-port=80/tcp --permanent

> firewall-cmd --reload

> nginx


#### Test load balance
> visit http://192.168.100.28 or http://192.168.100.29
```markdown
load balance should work if you see 192.168.100.30 and 192.168.100.32 in turn
```

#### Setup keepalived (192.168.100.28, 192.168.100.29)
> wget http://www.keepalived.org/software/keepalived-1.3.9.tar.gz

> tar zxvf keepalived-1.3.9.tar.gz

> cd keepalived-1.3.9

> ./configure

> yum install openssl openssl-devel -y

> ./configure 

> make

> make install

> ln -s /usr/local/sbin/keepalived /usr/sbin/

> vi /root/check_nginx.sh
```markdown
#!/bin/bash
if [ "$(ps -ef | grep "nginx: master process" | grep -v grep)" == "" ]
    then
        killall keepalived
    else
        echo "nginx is running"
fi
```

> vi /usr/local/etc/keepalived/keepalived.conf
```markdown
! Configuration File for keepalived

global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.200.1
   smtp_connect_timeout 30
   router_id LVS_DEVEL
   vrrp_skip_check_adv_addr
   vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
    state BACKUP
    interface eth0
    virtual_router_id 51
    priority 150
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.100.40
    }
}

virtual_server 192.168.100.40 80 {
    delay_loop 6
    lb_algo rr
    lb_kind DR
    persistence_timeout 50
    protocol TCP

    real_server 192.168.100.28 80 {
        weight 1
        TCP_CHECK {
            connect_timeout 3
            nb_get_retry 3
            delay_before_retry 3
            connect_port 80
        }
    }
    real_server 192.168.100.29 80 {
        weight 1
        TCP_CHECK {
            connect_timeout 3
            nb_get_retry 3
            delay_before_retry 3
            connect_port 80
        }
    }
}
```
> mkdir /etc/keepalived

> cp /usr/local/etc/keepalived/keepalived.conf /etc/keepalived/

> firewall-cmd --permanent --zone=public --add-rich-rule 'rule family="ipv4" source address="192.168.100.40/24" port port="80" protocol="tcp" accept'

> firewall-cmd --permanent --zone=public --add-rich-rule 'rule family="ipv4" source address="224.0.0.18" accept'

> firewall-cmd --reload

> systemctl start keepalived

> ip addr
you should see inet 192.168.100.40/32 under enp0s3
```markdown
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 08:00:27:fb:d0:a0 brd ff:ff:ff:ff:ff:ff
    inet 192.168.100.29/24 brd 192.168.100.255 scope global dynamic enp0s3
       valid_lft 81627sec preferred_lft 81627sec
    inet 192.168.100.40/32 scope global enp0s3
       valid_lft forever preferred_lft forever
```

#### Test keepalived
> visit http://192.168.100.40 should work

stop nginx on 192.168.100.28 or 192.168.100.29
> nginx -s stop

> visit http://192.168.100.40 should still work



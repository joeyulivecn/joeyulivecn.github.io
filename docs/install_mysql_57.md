  
  wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm  
  rpm -Uvh mysql57-community-release-el7-11.noarch.rpm  
  yum repolist  
  yum install mysql-community-server-5.7.22  
  vim /etc/my.cnf -> bind-address 0.0.0.0  
  systemctl start mysqld  
  cat /var/log/mysqld.log | grep 'temporary password'  
  mysql_secure_installation  
  mysql -uroot -p  
  update user set host='%' where user = 'root';  
  
  firewall-cmd --add-port=3306/tcp --permanent 
  firewall-cmd --reload 
  
  
  -- set global validate_password_policy=0;
  
 

  ##Reset root password   
  /etc/my.cnf -> restart mysqld
  skip-grant-tables

  mysql -uroot -p
  use mysql;

  update user set authentication_string=password('root') where user='root';


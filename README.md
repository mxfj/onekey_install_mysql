# onekey_install_mysql
```
cd /tmp
git clone https://github.com/mxfj/onekey_install_mysql.git
cd onekey_install_mysql
chmod +x install_mysql.sh
./install_mysql.sh
```
# install input example
```
输入要安装实例的版本: 5.7
输入要安装实例的路径: /data/mysql_3306
输入要安装实例的端口: 3306
输入要实例的内存大小: 1
```
# start
```
mysql -uroot -p123456 -S /tmp/mysql3306.sock

/usr/local/mysql/bin/mysqld --defaults-file=/data/mysql_3306/my3306.cnf &

```

# close
```
/usr/local/mysql/bin/mysqladmin -uroot -p123456 -S /tmp/mysql3306.sock shutdown
```

#!/bin/bash
echo "Hello Welcome this is a  mysqlserver install script!"
echo "######################install example########################"
echo "###         输入要安装实例的版本: 5.7                     ###"
echo "###         输入要安装实例的路径: /data/mysql_3306        ###"
echo "###         输入要安装实例的端口: 3306                    ###"
echo "###         输入要实例的内存大小: 1                       ###"
echo "#############################################################"
mv my3306.cnf /usr/local/src
mv mysql_install.py /usr/local/src
cd /usr/local/src
python mysql_install.py

#!/usr/bin/env  pyton
# -*- coding: UTF-8 -*-
###################################################
# @Author:       zhenghb
# @Create Date:  2023-03-10
# @Version:      V3

# 注意事项：1、提示没有MySQLdb模块,请通过命令 yum install MySQL-python -y安装
#          2、执行脚本需要依次输入mysql版本，安装路径和实例端口
#          3、脚本和配置文件mysql_install.zip需要放在/usr/local/src 目录下

import readline
import os
import sys
import time
import commands
try:
    import MySQLdb
except ImportError,e:
    print "%s，请使用命令:  yum install MySQL-python -y" % e
    sys.exit()


conf = '/usr/local/src/my3306.cnf'

def get_local_ip():
    get_ip = """/sbin/ip a |grep 'inet ' |grep -v '/32' |awk -F'[/ ]' '{print $6}' |grep -E "^10\.|^172\.(1[6789]|2[0-9]|3[01])\.|^192\.168\." |head -1"""
    ret = os.popen(get_ip).read().strip()
    return ret


#安装5.6版本
def install_mysql_5_6(dir, port,size):
    if not os.path.isdir("/usr/local/mysql"):
        print "\033[1;31;40m%s\033[0m" % "    mysql.tar.gz was not install, install mysql.tar.gz !"
        os.popen("cd /usr/local/src")
        os.popen("wget https://www.percona.com/downloads/Percona-Server-5.6/Percona-Server-5.6.34-79.1/binary/tarball/Percona-Server-5.6.34-rel79.1-Linux.x86_64.ssl101.tar.gz")
        os.popen(
            "tar xf Percona-Server-5.6.34-rel79.1-Linux.x86_64.ssl101.tar.gz -C /usr/local")
        os.popen(
            "ln -s /usr/local/Percona-Server-5.6.34-rel79.1-Linux.x86_64.ssl101  /usr/local/mysql")
        os.popen("yum -y install numactl")
    check_mysql(dir,port,size)
    instance_mysql_5_6(dir,port)
    connect_mysql_5_6(dir,port)

#安装5.7版本
def install_mysql_5_7(dir, port,size):
    if not os.path.isdir("/usr/local/mysql"):
        print "\033[1;31;40m%s\033[0m" % "    Mysql not install, install mysql !"
        os.popen("cd /usr/local/src")
        os.popen("wget https://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.30-33/binary/tarball/Percona-Server-5.7.30-33-Linux.x86_64.ssl101.tar.gz")
        os.popen(
            "tar xf Percona-Server-5.7.30-33-Linux.x86_64.ssl101.tar.gz -C /usr/local/")
        os.popen(
            " ln -s Percona-Server-5.7.30-33-Linux.x86_64.ssl101 /usr/local/mysql")
        os.popen("yum -y install numactl")
        os.popen("cp /usr/local/mysql/lib/mysql/libjemalloc.so /usr/lib64/")
    check_mysql(dir,port,size)
    instance_mysql_5_7(dir,port)
    connect_mysql_5_7(dir,port)
#解决python2.7的so文件问题
def repair_mysql_so():
    file_count = "cat /etc/ld.so.conf.d/mysql-x86_64.conf|grep /usr/local/mysql/lib |wc -l"
    file_count_exec = int(os.popen(file_count).read().strip())
    if file_count_exec == 0:
        f = open('/etc/ld.so.conf.d/mysql-x86_64.conf', 'a')
        f.write("/usr/local/mysql/lib")
        f.close()
        os.popen("ldconfig")
def check_mysql(dir,port,size):
    if os.popen("id mysql|wc -l").read().strip() == '0':
        print "mysql user is not exits,useradd it"
        os.popen("useradd mysql -s /sbin/nologin ")
        print "mysql 用户创建成功"
    if not os.path.isdir(dir):
        os.popen(
            "mkdir -p %s/{binlog,innodb_log,innodb_ts/undolog,mydata,tmpdir}" % dir)
        print "%s 目录创建成功" % dir
        os.popen("chown -R  mysql.mysql %s" % dir)
        os.popen("chown -R  mysql.mysql /usr/local/mysql")
        print "%s 目录授权成功" % dir
    if os.path.isfile(conf):
        inip = get_local_ip()
        #print inip
        inip = str(inip).split('.')[-1]
        os.popen("cp %s %s/my%s.cnf" % (conf, dir, port))
        os.popen("sed -i 's/\/data\/mysql\_3306/"+dir.replace("/","\/")+"/g' "+dir+"/my"+port+".cnf")
        #print "sed  -i 's/^.*server-id*$/server-id =" + inip + port+"/g' " + dir + "/my" + port + ".cnf"
        os.popen("sed  -i 's/^.*server-id.*$/server-id = " + inip + port+"/g' " + dir + "/my" + port + ".cnf")
        os.popen("sed  -i 's/^.*innodb_buffer_pool_size.*$/innodb_buffer_pool_size = " + size+ "G/g' " + dir + "/my" + port + ".cnf")
	os.popen("sed -i s/3306/%s/g  %s/my%s.cnf " % (port, dir, port))
    else:
        print "mysql.cnf 配置文件不存在/usr/local/src下!"
        sys.exit()

#初始化和启动mysql5.6
def instance_mysql_5_6(dir,port):
    if os.popen("netstat -lntp|grep %s|wc -l" % port).read().strip() != '0':
        print "mysql 端口 %s 已经存在!" % port
        sys.exit()
    else:
        print "%s 实例正在初始化........" % dir
        initialization = "/usr/local/mysql/scripts/mysql_install_db --defaults-file=%s/my%s.cnf --basedir=/usr/local/mysql/ --datadir=%s/mydata --user=mysql " % (
            dir, port, dir)
        result = commands.getstatusoutput(initialization)
        if result[0] == 0:
            print "%s 实例初始化成功" % dir
            if not os.path.islink("/bin/mysql"):
                os.popen("ln -s /usr/local/mysql/bin/*  /bin/")
            os.popen(
                "/usr/local/mysql/bin/mysqld --defaults-file=%s/my%s.cnf >/dev/null 2>&1 &" % (dir, port))
            if os.popen("ps -ef|grep %s |grep -v grep|wc -l" % port).read().strip() != '0':
                print "%s 实例启动成功" % dir
                time.sleep(10)
            else:
                print "%s 实例启动失败" % dir
                sys.exit()
        else:
            print "%s 实例初始化失败" % dir
            sys.exit()

#初始化和启动mysql5.7
def instance_mysql_5_7(dir,port):
    if os.popen("netstat -lntp|grep %s|wc -l" % port).read().strip() != '0':
        print "mysql 端口 %s 已经存在!" % port
        sys.exit()
    else:
        print "%s 实例正在初始化........" % dir
        initialization = "/usr/local/mysql/bin/mysqld --defaults-file=%s/my%s.cnf --basedir=/usr/local/mysql/ --datadir=%s/mydata --user=mysql --initialize-insecure" % (
            dir, port, dir)
        result = commands.getstatusoutput(initialization)
        if result[0] == 0:
            print "%s 实例初始化成功" % dir
            if not os.path.islink("/bin/mysql"):
                os.popen("ln -s /usr/local/mysql/bin/*  /bin/")
            os.popen(
                "/usr/local/mysql/bin/mysqld --defaults-file=%s/my%s.cnf &" % (dir, port))
            if os.popen("ps -ef|grep %s |grep -v grep|wc -l" % port).read().strip() != '0':
                print "%s 实例启动成功" % dir
                time.sleep(10)
            else:
                print "%s 实例启动失败" % dir
                sys.exit()
        else:
            print "%s 实例初始化失败" % dir
            sys.exit()

#mysql5.6修改密码
def connect_mysql_5_6(dir, port):
    sock = "/tmp/mysql" + port + ".sock"
    conn = MySQLdb.connect(unix_socket=sock, user="root", passwd="")
    cursor = conn.cursor()
    sql = "set password for 'root'@'localhost' = password('123456');"
    try:
        cursor.execute(sql)
        conn.commit()
        print "%s 实例密码修改成功,请登陆mysql实例!" % dir
    except Exception, e:
        print e
    cursor.close()
    conn.close()

#mysql5.7修改密码
def connect_mysql_5_7(dir, port):
    sock = "/tmp/mysql" + port + ".sock"
    conn = MySQLdb.connect(unix_socket=sock, user="root", passwd="")
    cursor = conn.cursor()
    sql = "alter user 'root'@'localhost' IDENTIFIED BY '123456';"
    try:
        cursor.execute(sql)
        conn.commit()
        print "%s 实例密码修改成功,请登陆mysql实例!" % dir
    except Exception, e:
        print e
    cursor.close()
    conn.close()

def main():
    version = raw_input('输入要安装实例的版本: ')
    if version == str(5.6):
        dir = raw_input('输入要安装实例的路径: ')
        port = raw_input('输入要安装实例的端口: ')
        size = raw_input('输入要实例的内存大小: ')
        install_mysql_5_6(dir, port,size)
        repair_mysql_so()
    elif version == str(5.7):
        dir = raw_input('输入要安装实例的路径: ')
        port = raw_input('输入要安装实例的端口: ')
        size = raw_input('输入要实例的内存大小: ')
        install_mysql_5_7(dir, port,size)
        repair_mysql_so()
    else:
        print "请输入你要安装的mysql版本: 5.6 or 5.7"
        sys.exit()

if __name__ == '__main__':
    main()

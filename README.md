# Introduction
Just a API of Blog-Admin and Blog-Web


# Installation
take a look at the manager.py file, Makefile, Procfile you will know it.
you can use your own way to run it, such as supervisro, uwsgi, gunicorn.
```
mkvirtualenv blog-venv
git clone https://github.com/yuchaoshui/blog
cd blog
make install-deps
make dist
```
use virtualenvwrapper to make a virtual env, then install dependency， then
make a python whl package like this `blog-0.0.1-py3-none-any.whl`. you can
install it use pip tool, `pip install blog-0.0.1-py3-none-any.whl`

# Commands
```
blog --help
```

# Generate rsa private key and public key
```
openssl genrsa -out auth.pem 512
openssl rsa -in auth.pem -pubout -out auth.pub
```
or there is another way to generate
```
openssl genpkey -out auth.pem -algorithm rsa -pkeyopt rsa_keygen_bits:512
openssl rsa -in auth.pem -out auth.pub -pubout
```
then overwrite two files in settings directory.


# Development
copy settings/default_settings.py to project root directory, rename it to .settings.py,
and you can overwrite default settings.

`make dist` to make a package,
`honcho start` to start server locally.
`make compile-deps` to generate requirements.txt use requirements.in



# Blog Admin
## register
Endpoint:
```
POST:/api/v1/user/register
```
Example Request Body:
```
{
	"nickname":"qinxiao",
	"email":"qinxiao@qq.com"
}
```
Example Response:
```
{
    "data": {
        "defaultPassword": "0123456789",
        "nickname": "qinxiao",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE1NTc3MjIzOTEsIm5iZiI6MTU1Njg1ODM5MSwidHRsIjo4NjQwMDAsImlhdCI6MTU1Njg1ODM5MSwiZGF0YSI6eyJ1c2VySWQiOjMsIm5pY2tuYW1lIjoicWlueGlhbyJ9LCJmb3JtYXQiOiJ1dGMifQ.TgVTw63TBdBlm0lmztOqV7AJOz6KswyQCxmB-dwxiP7PyX9nf4to4vSzQJwuzqkfa6h5btheQ-23Nn0yyKThDQ",
        "userId": 3
    },
    "err": "SUCCESS",
    "msg": ""
}
```
##  login
Endpoint:
```
POST:/api/v1/user/login
```
Example Request Body:
```
{
	"account":"qinxiao@qq.com",
	"password":"0123456789"
}
```
Example Response:
```
{
    "data": {
        "nickname": "qinxiao",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE1NTc3MjI3NjgsIm5iZiI6MTU1Njg1ODc2OCwidHRsIjo4NjQwMDAsImlhdCI6MTU1Njg1ODc2OCwiZGF0YSI6eyJ1c2VySWQiOjMsIm5pY2tuYW1lIjoicWlueGlhbyJ9LCJmb3JtYXQiOiJ1dGMifQ.f0yaFtVX6UmsuGL5O7tftNoG6d7GngbzFMbFvflLWTq0awjOJZObd9_TAIYcDndIejrBH6czLqhnK90bJhP2Sw",
        "userId": 3
    },
    "err": "SUCCESS",
    "msg": ""
}
```
## Article of Blog
### Get Articles List
Endpoint:
```
GET:/api/v1/admin/articles
```
Example Response:
```
{
    "data": {
        "articleList": [
            {
                "_id": 28,
                "category": "数据库",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "# 一、simple nested-loop join(SNLJ)\n- 从驱动表中取第一条记录，和被驱动表的所有记录比较判断。\n- 从驱动表中取第二条记录，和被驱动表的所有记录比较判断。\n- 直到驱动表的所有记录都和被驱动表的所有记录都比较完毕。\n- 比较次数是 M*N\n# 二、index nested-loop join(INLJ)\n- 通常，被驱动表建有索引，此时驱动表中的每一条记录通过被驱动表的索引进行访问。\n- 因为索引查询的成本是比较固定的，故MySQL优化器都倾向于使用记录数少的表作为驱动表。\n- 驱动表会根据被驱动表关联字段的索引进行查找，当在索引上找到了符合的值，再回表（被驱动表）进行查询，也就是只有当匹配到索引以后才会进行回表。\n- 比较次数M*index(N)\n# 三、block nested-loop join(BNLJ)\n- 通常情况下，mysql会先判断被驱动表是否有索引，如果没有索引则使用BNLJ。\n- 相较于SNLJ，BNLJ的改进就在于可以减少内表（被驱动表）的扫描次数，仅需扫描一次。\n- BNLJ多了一个中间处理过程，也就是join buffer，使用join buffer将驱动表的查询JOIN相关列都给缓冲到了JOIN BUFFER当中，然后批量与被驱动表进行比较，可以将多次比较合并到一次，降低了被驱动表的访问频率。\n- 在MySQL当中，我们可以通过参数join_buffer_size来设置join buffer的值，然后再进行操作，默认情况下join_buffer_size=256K。\n- 在查找的时候MySQL会将所有需要的列缓存到join buffer当中，包括select的列，而不是仅仅只缓存关联列。\n- 在一个有N个JOIN关联的SQL当中会在执行时候分配N-1个join buffer。 \n\n# 四、使用场景\n1、如果使用left join语句，则left join 前的表设置为驱动表，left join 后的表设置为被驱动表，被驱动表如果没加索引，效率会非常低\n\n2、使用inner join 连接表语句，则mysql会自动优化， 将加索引的表设置为被驱动表，未加索引的表设为驱动表\n\n3、两个表都存在索引的情况下，小表驱动大表查询效果更好",
                "summary": "MySQL 的连表查询我们经常使用，合理的使用连表查询会大大提升查询速度。MySQL使用的是一种叫做嵌套循环连接。",
                "tags": [
                    "mysql"
                ],
                "title": "MySQL连接查询原理",
                "viewTimes": 0
            },
            {
                "_id": 29,
                "category": "数据库",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "## 1、下载，解压，编译\n```\n# wget http://download.redis.io/releases/redis-3.2.6.tar.gz\n# tar -zxvf redis-3.2.6.tar.gz -C /usr/local/\n# mv redis-3.2.6  redis\n# cd redis\n# make\n# make install\n```\nmake是编译，make install 是把redis相关的命令拷贝到/usr/local/bin/这个目录下面。二进制文件编译完成后是在src目录下。 \n- 注意： make install 的作用仅仅是把要用到的可执行命令拷贝到/usr/local/bin/下面，如果不需要拷贝，可不运行该命令，启动是都用全局命令执行。\n\n## 2、编辑配置文件、创建数据目录\n```\n# cp /usr/local/redis/redis.conf  /usr/local/redis/redis_9333.conf\n# vim /usr/local/redis/redis_9333.conf\n```\n通常情况下，我们会把配置文件的名字上加上端口以便于区分，修改下面的配置，这些配置都是一个端口的，因为同一台机器可能会启多个redis，所以这样可以把数据更好滴分开。也可以不使用下面的配置，但是这样做有很大的好处的。\n```\nport  9333\npidfile /var/run/redis_9333.pid\ndaemonize yes\ndbfilename dump_9333.rdb\ndir /data/\nmaxclients 50000\nlogfile \"/var/log/redis_9333.log\"\nappendonly yes\nappendfilename \"appendonly_9333.aof\"\n```\n## 3、创建数据目录，启动redis，启动刚才配置的9333端口的redis\n```\n# mkdir /data\n# redis-server /usr/local/redis/redis_9333.conf\n```\n或者如果没有运行 `make install` 命令安装的话，使用全局路径启动，然后加入开机自启动里面。\n```\n# /usr/local/redis/src/redis-server /usr/local/redis/redis_9333.conf\n```\n4、登录redis\n如果不是本地连接，而是远程连接的话，加 -h 参数指定服务器的IP。\n```\n# redis-cli -p 9333 -h 127.0.0.1\n127.0.0.1:9333> ping\nPONG\n127.0.0.1:9333>info\n```\nOK，安装配置成功！\n",
                "summary": "Redis 安装是最简单的，只需要下载源码包，make、make install 即可，但是要有非常稳定的Redis服务的话，还需要做一下简单的配置，后面会给出这些配置信息。",
                "tags": [
                    "redis"
                ],
                "title": "Redis安装及常用配置",
                "viewTimes": 0
            },
            {
                "_id": 30,
                "category": "操作系统",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "## 一、同步互联网时间\n一次运行以下命令配置修改时区，根据提示进行配置。\n```\n# tzselect\n# cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime\n# hwclock --systohc\n```\n\n运行ntpdate命令同步时间，以下任一时间服务器都可使用，任选一个即可。\n```\n# ntpdate  time1.aliyun.com\n# ntpdate  time2.aliyun.com\n# ntpdate  time3.aliyun.com\n# ntpdate  time4.aliyun.com\n# ntpdate  time5.aliyun.com\n# ntpdate  time6.aliyun.com\n# ntpdate  time7.aliyun.com\n```\n\n## 二、取消、设置自动从互联网同步时间\n现在如果系统默认是同步了网络时间的，假如你不想同步互联网时间，可通过下面命令取消、开启。\n```\n# timedatectl set-ntp 0\n# timedatectl set-ntp 1\n```\n\n## 三、修改系统日期时间\n修改为字符串提供的时间字符串。\n```\n# date -s \"2018-04-10\"\n# date -s \"10:10:20\"\n# date -s \"2018-04-10 10:10:20\"\n# hwclock --systohc\n```",
                "summary": "同步互联网时间",
                "tags": [
                    "Ubuntu"
                ],
                "title": "Ubuntu 时间设置",
                "viewTimes": 0
            },
            {
                "_id": 31,
                "category": "编程之路",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "## 一、普通 MySQL 连接方法\n使用模块 MySQLdb 普通方式连接。\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nimport MySQLdb\nconn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='test')\ncursor = conn.cursor()\nsql_1 = \"select * from user where id = %s;\" % (5,)\nsql_2 = \"select * from user \\\n         where id = %s;\" % (5,)\nsql_3 = \"\"\"\n           insert into user(username, password)\n           values(\"yuchaoshui\", \"123\");\n        \"\"\"\ntry:\n    print cursor.execute(sql_1)\n    print cursor.fetchall()\n    print cursor.execute(sql_2)\n    print cursor.fetchall()\n    print cursor.execute(sql_3)\n    conn.commit()\nexcept Exception as e:\n    print(e)\n    conn.rollback()\ncursor.close()\nconn.close()\n```\n execute() 返回结果表示影响的行数。cursor.fetchone() 取回一条结果。sql_1 直接一行写完，sql_2 换行写完， sql_3 多行写。 查询时不需要 commit() 操作，插入、更新、删除时需要 commit() 提交。 \n\n\n## 二、使用连接池连接MySQL\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nimport MySQLdb\nfrom DBUtils.PooledDB import PooledDB\npool = PooledDB(MySQLdb, 5, host='127.0.0.1', port=3306, user='root', passwd='123', db='test')\nconn = pool.connection()\ncursor = conn.cursor()\nsql_1 = \"select * from user where id = %s;\" % (5,)\nsql_2 = \"select * from user \\\n         where id = %s;\" % (5,)\nsql_3 = \"\"\"\n           insert into user(username, password)\n           values(\"yuchaoshui\", \"123\");\n        \"\"\"\ntry:\n    print cursor.execute(sql_1)\n    print cursor.fetchall()\n    print cursor.execute(sql_2)\n    print cursor.fetchall()\n    print cursor.execute(sql_3)\n    conn.commit()\nexcept Exception as e:\n    print(e)\n    conn.rollback()\ncursor.close()\nconn.close()\n```\n5 为连接池里的最少连接数， 以后每次需要数据库连接就是用connection()函数获取连接就好了 \n\n\nPooledDB 的默认值\n```\nPooledDB(self, creator, mincached=0, maxcached=0, maxshared=0, maxconnections=0, blocking=False, maxusage=None, setsession=None, reset=True, failures=None, ping=1, *args, **kwargs)\n```\nPooledDB的参数： \nmincached，最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接\nmaxcached，最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接\nmaxconnections，最大的连接数，\nblocking，当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，直到当前连接数小于最大连接数，如果这个值是False，会报错，\nmaxshared , 当连接数达到这个数，新请求的连接会分享已经分配出去的连接 \n\n## 三、模块导入连接 MySQL\n  以连接池的方式，编写模块 mysqlhelper.py，可以在项目的其他地方导入MySQL连接实例即可使用。 模块点此下载\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nfrom __future__ import print_function\nfrom DBUtils.PooledDB import PooledDB\nimport MySQLdb\nimport sys\n__all__ = ['m'] + [\"m\"+str(i) for i in range(2, 11)]\nclass MH(object):\n    def __init__(self):\n        try:\n            print(\"Connecting MySQL Server {0}@{1}:{2} ..\".format(\n                self.__class__.db, self.__class__.host, self.__class__.port), end='.')\n            self.conn = self.__class__.pool.connection()\n            self.cursor = self.conn.cursor()\n            print(' ok!')\n        except Exception, e:\n            print(\"pool.connection error: {0}\".format(e))\n    def select(self, query=''):\n        try:\n            self.effect = self.cursor.execute(query)\n            return self.cursor\n        except Exception as e:\n            print(\"select error: {0}\".format(e))\n    def update(self, query=''):\n        try:\n            self.effect = self.cursor.execute(query)\n            self.conn.commit()\n        except Exception as e:\n            print(\"update error: {0}\".format(e))\n            self.conn.rollback()\n            self.effect = 0\n# M2 类继承自 M1，表示一个新的 MySQL 连接池。\n# 如果需要新的连接池 ，按照如下格式新增即可。\nclass MH2(MH):\n    pass\ndef init_pool(M,\n            host='127.0.0.1', \n            port=3306, \n            user='root', \n            password='', \n            database='test',\n            pool_size=5): \n    M.host = host\n    M.port = int(port)\n    M.user = user\n    M.password = password\n    M.db = database\n    M.pool_size = pool_size\n    try:\n        M.pool = PooledDB(MySQLdb, \n            M.pool_size,\n            host=M.host,\n            port=M.port,\n            user=M.user,\n            passwd=M.password,\n            db=M.db)\n    except Exception, e:\n        print(\"PooledDB init error: {0}\".format(e))\n        exit(1)\n# 初始化连接池，可以有多个。第一个参数是前面手动定义的连接池类。\ninit_pool(MH, '127.0.0.1', 3306, 'root', '123', 'test')\ninit_pool(MH2, '12.55.5.61', 3306, 'root', '123', 'test')\n# 定义将要被导出的MySQL实例。 一个连接池可同时提供多个实例对象。\nm = MH()\nm2 = MH2()\nif __name__ == \"__main__\":\n    pass\n    #print \"\\nm info:\"\n    #print m.select(\"select * from user;\").fetchone()\n    #print m.effect\n    #print m.select(\"select * from user;\").fetchall()\n    #print m.effect\n    #m.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    #print m.effect\n    ##################################################\n    #print \"\\nm2 info:\"\n    #print m2.select(\"select * from user;\").fetchone()\n    #print m2.effect\n    #print m2.select(\"select * from user;\").fetchall()\n    #print m2.effect\n    #m2.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    #print m2.effect\n```\n\n使用方法\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nfrom mysqlhelper import m, m2\nimport time\ndef test():\n    print \"\\nm info:\"\n    print m.select(\"select * from user;\").fetchone()\n    print m.effect\n    print m.select(\"select * from user;\").fetchall()\n    print m.effect\n    m.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    print m.effect\n    #################################################\n    print \"\\nm2 info:\"\n    print m2.select(\"select * from user;\").fetchone()\n    print m2.effect\n    print m2.select(\"select * from user;\").fetchall()\n    print m2.effect\n    m2.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    print m2.effect\nif __name__ == '__main__':\n    test()\n```",
                "summary": "Python 连接 MySQL的三种方式",
                "tags": [
                    "mysql",
                    "python"
                ],
                "title": "Python 连接 MySQL",
                "viewTimes": 0
            }
        ],
        "categories": [
            "操作系统",
            "数据库",
            "数据结构",
            "编程之路",
            "计算机组成原理"
        ],
        "tags": [
            "mysql",
            "python",
            "redis",
            "Ubuntu"
        ]
    },
    "err": "SUCCESS",
    "msg": ""
}
```
### Write Article
Endpoint:
```
POST:/api/v1/admin/articles
```
Example Request Body:
```
{
	"title":"supervisor",
	"summary":"后台进程管理工具 supervisor 使用总结",
	"markdownContent":"superviosr 是一个 Linux/Unix 系统上的进程管理工具，可以管理和监控 Linux 上面的进程，能将一个普通的命令行进程变为后台 daemon，并监控进程状态，异常退出时能自动重启，它不能监控 daemon 进程。",
	"tags":["Linux"],
	"category":"操作系统"
}
```
###  Delete Article
Endpoint:
```
DELETE:/api/v1/admin/articles
```
Example Request Body:
```
{
	"id":32
}
```

## category
### Get Categories
Endpoint:
```
GET:/api/v1/admin/categories
```
Example Response:
```
{
    "data": {
        "categories": [
            "操作系统",
            "数据库",
            "数据结构",
            "编程之路",
            "计算机组成原理",
            "计算机网络"
        ]
    },
    "err": "SUCCESS",
    "msg": ""
}
```
### Add Category
Endpoint:
```
POST：/api/v1/admin/categories
```
Example Request Body:
```
{
	"name":"计算机组成原理"
}
```

### Delete Category
Endpoint:
```
DELETE:/api/v1/admin/categories
```
Example Request Body:
```
{
	"name":"计算机网络"
}
```

## Tag
### Get Tags
Endpoint:
```
GET:/api/v1/admin/tags
```
Example Response:
```

{
    "data": {
        "tags": [
            "mysql",
            "python",
            "redis",
            "Ubuntu"
        ]
    },
    "err": "SUCCESS",
    "msg": ""
}
```
### Add Tag
Endpoint:
```
POST:/api/v1/admin/tags
```
Example Request Body:
```
{
	"name":"C++"
}
```
### Delete Tag
Endpoint:
```
DELETE:/api/v1/admin/tags
```
Example Request Body:
```
{
	"name":"C++"
}
```


# Blog Web
## Get Articles List
Endpoint:
```
GET:/api/v1/articles/<string:nickname>
```
Example Response:
```
{
    "data": {
        "articleList": [
            {
                "_id": 28,
                "category": "数据库",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "# 一、simple nested-loop join(SNLJ)\n- 从驱动表中取第一条记录，和被驱动表的所有记录比较判断。\n- 从驱动表中取第二条记录，和被驱动表的所有记录比较判断。\n- 直到驱动表的所有记录都和被驱动表的所有记录都比较完毕。\n- 比较次数是 M*N\n# 二、index nested-loop join(INLJ)\n- 通常，被驱动表建有索引，此时驱动表中的每一条记录通过被驱动表的索引进行访问。\n- 因为索引查询的成本是比较固定的，故MySQL优化器都倾向于使用记录数少的表作为驱动表。\n- 驱动表会根据被驱动表关联字段的索引进行查找，当在索引上找到了符合的值，再回表（被驱动表）进行查询，也就是只有当匹配到索引以后才会进行回表。\n- 比较次数M*index(N)\n# 三、block nested-loop join(BNLJ)\n- 通常情况下，mysql会先判断被驱动表是否有索引，如果没有索引则使用BNLJ。\n- 相较于SNLJ，BNLJ的改进就在于可以减少内表（被驱动表）的扫描次数，仅需扫描一次。\n- BNLJ多了一个中间处理过程，也就是join buffer，使用join buffer将驱动表的查询JOIN相关列都给缓冲到了JOIN BUFFER当中，然后批量与被驱动表进行比较，可以将多次比较合并到一次，降低了被驱动表的访问频率。\n- 在MySQL当中，我们可以通过参数join_buffer_size来设置join buffer的值，然后再进行操作，默认情况下join_buffer_size=256K。\n- 在查找的时候MySQL会将所有需要的列缓存到join buffer当中，包括select的列，而不是仅仅只缓存关联列。\n- 在一个有N个JOIN关联的SQL当中会在执行时候分配N-1个join buffer。 \n\n# 四、使用场景\n1、如果使用left join语句，则left join 前的表设置为驱动表，left join 后的表设置为被驱动表，被驱动表如果没加索引，效率会非常低\n\n2、使用inner join 连接表语句，则mysql会自动优化， 将加索引的表设置为被驱动表，未加索引的表设为驱动表\n\n3、两个表都存在索引的情况下，小表驱动大表查询效果更好",
                "summary": "MySQL 的连表查询我们经常使用，合理的使用连表查询会大大提升查询速度。MySQL使用的是一种叫做嵌套循环连接。",
                "tags": [
                    "mysql"
                ],
                "title": "MySQL连接查询原理",
                "viewTimes": 0
            },
            {
                "_id": 29,
                "category": "数据库",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "## 1、下载，解压，编译\n```\n# wget http://download.redis.io/releases/redis-3.2.6.tar.gz\n# tar -zxvf redis-3.2.6.tar.gz -C /usr/local/\n# mv redis-3.2.6  redis\n# cd redis\n# make\n# make install\n```\nmake是编译，make install 是把redis相关的命令拷贝到/usr/local/bin/这个目录下面。二进制文件编译完成后是在src目录下。 \n- 注意： make install 的作用仅仅是把要用到的可执行命令拷贝到/usr/local/bin/下面，如果不需要拷贝，可不运行该命令，启动是都用全局命令执行。\n\n## 2、编辑配置文件、创建数据目录\n```\n# cp /usr/local/redis/redis.conf  /usr/local/redis/redis_9333.conf\n# vim /usr/local/redis/redis_9333.conf\n```\n通常情况下，我们会把配置文件的名字上加上端口以便于区分，修改下面的配置，这些配置都是一个端口的，因为同一台机器可能会启多个redis，所以这样可以把数据更好滴分开。也可以不使用下面的配置，但是这样做有很大的好处的。\n```\nport  9333\npidfile /var/run/redis_9333.pid\ndaemonize yes\ndbfilename dump_9333.rdb\ndir /data/\nmaxclients 50000\nlogfile \"/var/log/redis_9333.log\"\nappendonly yes\nappendfilename \"appendonly_9333.aof\"\n```\n## 3、创建数据目录，启动redis，启动刚才配置的9333端口的redis\n```\n# mkdir /data\n# redis-server /usr/local/redis/redis_9333.conf\n```\n或者如果没有运行 `make install` 命令安装的话，使用全局路径启动，然后加入开机自启动里面。\n```\n# /usr/local/redis/src/redis-server /usr/local/redis/redis_9333.conf\n```\n4、登录redis\n如果不是本地连接，而是远程连接的话，加 -h 参数指定服务器的IP。\n```\n# redis-cli -p 9333 -h 127.0.0.1\n127.0.0.1:9333> ping\nPONG\n127.0.0.1:9333>info\n```\nOK，安装配置成功！\n",
                "summary": "Redis 安装是最简单的，只需要下载源码包，make、make install 即可，但是要有非常稳定的Redis服务的话，还需要做一下简单的配置，后面会给出这些配置信息。",
                "tags": [
                    "redis"
                ],
                "title": "Redis安装及常用配置",
                "viewTimes": 0
            },
            {
                "_id": 30,
                "category": "操作系统",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "## 一、同步互联网时间\n一次运行以下命令配置修改时区，根据提示进行配置。\n```\n# tzselect\n# cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime\n# hwclock --systohc\n```\n\n运行ntpdate命令同步时间，以下任一时间服务器都可使用，任选一个即可。\n```\n# ntpdate  time1.aliyun.com\n# ntpdate  time2.aliyun.com\n# ntpdate  time3.aliyun.com\n# ntpdate  time4.aliyun.com\n# ntpdate  time5.aliyun.com\n# ntpdate  time6.aliyun.com\n# ntpdate  time7.aliyun.com\n```\n\n## 二、取消、设置自动从互联网同步时间\n现在如果系统默认是同步了网络时间的，假如你不想同步互联网时间，可通过下面命令取消、开启。\n```\n# timedatectl set-ntp 0\n# timedatectl set-ntp 1\n```\n\n## 三、修改系统日期时间\n修改为字符串提供的时间字符串。\n```\n# date -s \"2018-04-10\"\n# date -s \"10:10:20\"\n# date -s \"2018-04-10 10:10:20\"\n# hwclock --systohc\n```",
                "summary": "同步互联网时间",
                "tags": [
                    "Ubuntu"
                ],
                "title": "Ubuntu 时间设置",
                "viewTimes": 0
            },
            {
                "_id": 31,
                "category": "编程之路",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "## 一、普通 MySQL 连接方法\n使用模块 MySQLdb 普通方式连接。\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nimport MySQLdb\nconn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='test')\ncursor = conn.cursor()\nsql_1 = \"select * from user where id = %s;\" % (5,)\nsql_2 = \"select * from user \\\n         where id = %s;\" % (5,)\nsql_3 = \"\"\"\n           insert into user(username, password)\n           values(\"yuchaoshui\", \"123\");\n        \"\"\"\ntry:\n    print cursor.execute(sql_1)\n    print cursor.fetchall()\n    print cursor.execute(sql_2)\n    print cursor.fetchall()\n    print cursor.execute(sql_3)\n    conn.commit()\nexcept Exception as e:\n    print(e)\n    conn.rollback()\ncursor.close()\nconn.close()\n```\n execute() 返回结果表示影响的行数。cursor.fetchone() 取回一条结果。sql_1 直接一行写完，sql_2 换行写完， sql_3 多行写。 查询时不需要 commit() 操作，插入、更新、删除时需要 commit() 提交。 \n\n\n## 二、使用连接池连接MySQL\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nimport MySQLdb\nfrom DBUtils.PooledDB import PooledDB\npool = PooledDB(MySQLdb, 5, host='127.0.0.1', port=3306, user='root', passwd='123', db='test')\nconn = pool.connection()\ncursor = conn.cursor()\nsql_1 = \"select * from user where id = %s;\" % (5,)\nsql_2 = \"select * from user \\\n         where id = %s;\" % (5,)\nsql_3 = \"\"\"\n           insert into user(username, password)\n           values(\"yuchaoshui\", \"123\");\n        \"\"\"\ntry:\n    print cursor.execute(sql_1)\n    print cursor.fetchall()\n    print cursor.execute(sql_2)\n    print cursor.fetchall()\n    print cursor.execute(sql_3)\n    conn.commit()\nexcept Exception as e:\n    print(e)\n    conn.rollback()\ncursor.close()\nconn.close()\n```\n5 为连接池里的最少连接数， 以后每次需要数据库连接就是用connection()函数获取连接就好了 \n\n\nPooledDB 的默认值\n```\nPooledDB(self, creator, mincached=0, maxcached=0, maxshared=0, maxconnections=0, blocking=False, maxusage=None, setsession=None, reset=True, failures=None, ping=1, *args, **kwargs)\n```\nPooledDB的参数： \nmincached，最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接\nmaxcached，最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接\nmaxconnections，最大的连接数，\nblocking，当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，直到当前连接数小于最大连接数，如果这个值是False，会报错，\nmaxshared , 当连接数达到这个数，新请求的连接会分享已经分配出去的连接 \n\n## 三、模块导入连接 MySQL\n  以连接池的方式，编写模块 mysqlhelper.py，可以在项目的其他地方导入MySQL连接实例即可使用。 模块点此下载\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nfrom __future__ import print_function\nfrom DBUtils.PooledDB import PooledDB\nimport MySQLdb\nimport sys\n__all__ = ['m'] + [\"m\"+str(i) for i in range(2, 11)]\nclass MH(object):\n    def __init__(self):\n        try:\n            print(\"Connecting MySQL Server {0}@{1}:{2} ..\".format(\n                self.__class__.db, self.__class__.host, self.__class__.port), end='.')\n            self.conn = self.__class__.pool.connection()\n            self.cursor = self.conn.cursor()\n            print(' ok!')\n        except Exception, e:\n            print(\"pool.connection error: {0}\".format(e))\n    def select(self, query=''):\n        try:\n            self.effect = self.cursor.execute(query)\n            return self.cursor\n        except Exception as e:\n            print(\"select error: {0}\".format(e))\n    def update(self, query=''):\n        try:\n            self.effect = self.cursor.execute(query)\n            self.conn.commit()\n        except Exception as e:\n            print(\"update error: {0}\".format(e))\n            self.conn.rollback()\n            self.effect = 0\n# M2 类继承自 M1，表示一个新的 MySQL 连接池。\n# 如果需要新的连接池 ，按照如下格式新增即可。\nclass MH2(MH):\n    pass\ndef init_pool(M,\n            host='127.0.0.1', \n            port=3306, \n            user='root', \n            password='', \n            database='test',\n            pool_size=5): \n    M.host = host\n    M.port = int(port)\n    M.user = user\n    M.password = password\n    M.db = database\n    M.pool_size = pool_size\n    try:\n        M.pool = PooledDB(MySQLdb, \n            M.pool_size,\n            host=M.host,\n            port=M.port,\n            user=M.user,\n            passwd=M.password,\n            db=M.db)\n    except Exception, e:\n        print(\"PooledDB init error: {0}\".format(e))\n        exit(1)\n# 初始化连接池，可以有多个。第一个参数是前面手动定义的连接池类。\ninit_pool(MH, '127.0.0.1', 3306, 'root', '123', 'test')\ninit_pool(MH2, '12.55.5.61', 3306, 'root', '123', 'test')\n# 定义将要被导出的MySQL实例。 一个连接池可同时提供多个实例对象。\nm = MH()\nm2 = MH2()\nif __name__ == \"__main__\":\n    pass\n    #print \"\\nm info:\"\n    #print m.select(\"select * from user;\").fetchone()\n    #print m.effect\n    #print m.select(\"select * from user;\").fetchall()\n    #print m.effect\n    #m.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    #print m.effect\n    ##################################################\n    #print \"\\nm2 info:\"\n    #print m2.select(\"select * from user;\").fetchone()\n    #print m2.effect\n    #print m2.select(\"select * from user;\").fetchall()\n    #print m2.effect\n    #m2.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    #print m2.effect\n```\n\n使用方法\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nfrom mysqlhelper import m, m2\nimport time\ndef test():\n    print \"\\nm info:\"\n    print m.select(\"select * from user;\").fetchone()\n    print m.effect\n    print m.select(\"select * from user;\").fetchall()\n    print m.effect\n    m.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    print m.effect\n    #################################################\n    print \"\\nm2 info:\"\n    print m2.select(\"select * from user;\").fetchone()\n    print m2.effect\n    print m2.select(\"select * from user;\").fetchall()\n    print m2.effect\n    m2.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    print m2.effect\nif __name__ == '__main__':\n    test()\n```",
                "summary": "Python 连接 MySQL的三种方式",
                "tags": [
                    "mysql",
                    "python"
                ],
                "title": "Python 连接 MySQL",
                "viewTimes": 0
            }
        ],
        "categories": [
            "操作系统",
            "数据库",
            "数据结构",
            "编程之路",
            "计算机组成原理"
        ],
        "tags": [
            "Linux",
            "mysql",
            "python",
            "redis",
            "Ubuntu"
        ]
    },
    "err": "SUCCESS",
    "msg": ""
}
```
### Get Tag
Endpoint:
```
GET:/api/v1/tags/getList/<string:nickname>

```
Example Response:
```
{
    "data": {
        "tagList": [
            {
                "count": 0,
                "name": "C"
            },
            {
                "count": 0,
                "name": "C++"
            },
            {
                "count": 1,
                "name": "Linux"
            },
            {
                "count": 2,
                "name": "mysql"
            },
            {
                "count": 1,
                "name": "python"
            },
            {
                "count": 1,
                "name": "redis"
            },
            {
                "count": 1,
                "name": "Ubuntu"
            }
        ]
    },
    "err": "SUCCESS",
    "msg": ""
}
```
### Get Categories
```
GET:/api/v1/categories/getList/<string:nickname>
```
Example Response:
```
{
    "data": {
        "categoryList": [
            {
                "count": 2,
                "name": "操作系统"
            },
            {
                "count": 2,
                "name": "数据库"
            },
            {
                "count": 0,
                "name": "数据结构"
            },
            {
                "count": 1,
                "name": "编程之路"
            },
            {
                "count": 0,
                "name": "计算机组成原理"
            },
            {
                "count": 0,
                "name": "计算机网络"
            }
        ]
    },
    "err": "SUCCESS",
    "msg": ""
}

```
### Get Articles of category
```
GET:/api/v1/articles/category/<string:nickname>
```
Example Response:
```
{
    "data": {
        "articleList": [
            {
                "_id": 28,
                "category": "数据库",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "# 一、simple nested-loop join(SNLJ)\n- 从驱动表中取第一条记录，和被驱动表的所有记录比较判断。\n- 从驱动表中取第二条记录，和被驱动表的所有记录比较判断。\n- 直到驱动表的所有记录都和被驱动表的所有记录都比较完毕。\n- 比较次数是 M*N\n# 二、index nested-loop join(INLJ)\n- 通常，被驱动表建有索引，此时驱动表中的每一条记录通过被驱动表的索引进行访问。\n- 因为索引查询的成本是比较固定的，故MySQL优化器都倾向于使用记录数少的表作为驱动表。\n- 驱动表会根据被驱动表关联字段的索引进行查找，当在索引上找到了符合的值，再回表（被驱动表）进行查询，也就是只有当匹配到索引以后才会进行回表。\n- 比较次数M*index(N)\n# 三、block nested-loop join(BNLJ)\n- 通常情况下，mysql会先判断被驱动表是否有索引，如果没有索引则使用BNLJ。\n- 相较于SNLJ，BNLJ的改进就在于可以减少内表（被驱动表）的扫描次数，仅需扫描一次。\n- BNLJ多了一个中间处理过程，也就是join buffer，使用join buffer将驱动表的查询JOIN相关列都给缓冲到了JOIN BUFFER当中，然后批量与被驱动表进行比较，可以将多次比较合并到一次，降低了被驱动表的访问频率。\n- 在MySQL当中，我们可以通过参数join_buffer_size来设置join buffer的值，然后再进行操作，默认情况下join_buffer_size=256K。\n- 在查找的时候MySQL会将所有需要的列缓存到join buffer当中，包括select的列，而不是仅仅只缓存关联列。\n- 在一个有N个JOIN关联的SQL当中会在执行时候分配N-1个join buffer。 \n\n# 四、使用场景\n1、如果使用left join语句，则left join 前的表设置为驱动表，left join 后的表设置为被驱动表，被驱动表如果没加索引，效率会非常低\n\n2、使用inner join 连接表语句，则mysql会自动优化， 将加索引的表设置为被驱动表，未加索引的表设为驱动表\n\n3、两个表都存在索引的情况下，小表驱动大表查询效果更好",
                "summary": "MySQL 的连表查询我们经常使用，合理的使用连表查询会大大提升查询速度。MySQL使用的是一种叫做嵌套循环连接。",
                "tags": [
                    "mysql"
                ],
                "title": "MySQL连接查询原理",
                "viewTimes": 0
            },
            {
                "_id": 29,
                "category": "数据库",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "## 1、下载，解压，编译\n```\n# wget http://download.redis.io/releases/redis-3.2.6.tar.gz\n# tar -zxvf redis-3.2.6.tar.gz -C /usr/local/\n# mv redis-3.2.6  redis\n# cd redis\n# make\n# make install\n```\nmake是编译，make install 是把redis相关的命令拷贝到/usr/local/bin/这个目录下面。二进制文件编译完成后是在src目录下。 \n- 注意： make install 的作用仅仅是把要用到的可执行命令拷贝到/usr/local/bin/下面，如果不需要拷贝，可不运行该命令，启动是都用全局命令执行。\n\n## 2、编辑配置文件、创建数据目录\n```\n# cp /usr/local/redis/redis.conf  /usr/local/redis/redis_9333.conf\n# vim /usr/local/redis/redis_9333.conf\n```\n通常情况下，我们会把配置文件的名字上加上端口以便于区分，修改下面的配置，这些配置都是一个端口的，因为同一台机器可能会启多个redis，所以这样可以把数据更好滴分开。也可以不使用下面的配置，但是这样做有很大的好处的。\n```\nport  9333\npidfile /var/run/redis_9333.pid\ndaemonize yes\ndbfilename dump_9333.rdb\ndir /data/\nmaxclients 50000\nlogfile \"/var/log/redis_9333.log\"\nappendonly yes\nappendfilename \"appendonly_9333.aof\"\n```\n## 3、创建数据目录，启动redis，启动刚才配置的9333端口的redis\n```\n# mkdir /data\n# redis-server /usr/local/redis/redis_9333.conf\n```\n或者如果没有运行 `make install` 命令安装的话，使用全局路径启动，然后加入开机自启动里面。\n```\n# /usr/local/redis/src/redis-server /usr/local/redis/redis_9333.conf\n```\n4、登录redis\n如果不是本地连接，而是远程连接的话，加 -h 参数指定服务器的IP。\n```\n# redis-cli -p 9333 -h 127.0.0.1\n127.0.0.1:9333> ping\nPONG\n127.0.0.1:9333>info\n```\nOK，安装配置成功！\n",
                "summary": "Redis 安装是最简单的，只需要下载源码包，make、make install 即可，但是要有非常稳定的Redis服务的话，还需要做一下简单的配置，后面会给出这些配置信息。",
                "tags": [
                    "redis"
                ],
                "title": "Redis安装及常用配置",
                "viewTimes": 0
            }
        ]
    },
    "err": "SUCCESS",
    "msg": ""
}
```
### Get Articles of Tag
Endpoint:
```
GET:/api/v1/articles/tag/<string:nickname>/<string:tag>
```
Example Response:
```
{
    "data": {
        "articleList": [
            {
                "_id": 28,
                "category": "数据库",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "# 一、simple nested-loop join(SNLJ)\n- 从驱动表中取第一条记录，和被驱动表的所有记录比较判断。\n- 从驱动表中取第二条记录，和被驱动表的所有记录比较判断。\n- 直到驱动表的所有记录都和被驱动表的所有记录都比较完毕。\n- 比较次数是 M*N\n# 二、index nested-loop join(INLJ)\n- 通常，被驱动表建有索引，此时驱动表中的每一条记录通过被驱动表的索引进行访问。\n- 因为索引查询的成本是比较固定的，故MySQL优化器都倾向于使用记录数少的表作为驱动表。\n- 驱动表会根据被驱动表关联字段的索引进行查找，当在索引上找到了符合的值，再回表（被驱动表）进行查询，也就是只有当匹配到索引以后才会进行回表。\n- 比较次数M*index(N)\n# 三、block nested-loop join(BNLJ)\n- 通常情况下，mysql会先判断被驱动表是否有索引，如果没有索引则使用BNLJ。\n- 相较于SNLJ，BNLJ的改进就在于可以减少内表（被驱动表）的扫描次数，仅需扫描一次。\n- BNLJ多了一个中间处理过程，也就是join buffer，使用join buffer将驱动表的查询JOIN相关列都给缓冲到了JOIN BUFFER当中，然后批量与被驱动表进行比较，可以将多次比较合并到一次，降低了被驱动表的访问频率。\n- 在MySQL当中，我们可以通过参数join_buffer_size来设置join buffer的值，然后再进行操作，默认情况下join_buffer_size=256K。\n- 在查找的时候MySQL会将所有需要的列缓存到join buffer当中，包括select的列，而不是仅仅只缓存关联列。\n- 在一个有N个JOIN关联的SQL当中会在执行时候分配N-1个join buffer。 \n\n# 四、使用场景\n1、如果使用left join语句，则left join 前的表设置为驱动表，left join 后的表设置为被驱动表，被驱动表如果没加索引，效率会非常低\n\n2、使用inner join 连接表语句，则mysql会自动优化， 将加索引的表设置为被驱动表，未加索引的表设为驱动表\n\n3、两个表都存在索引的情况下，小表驱动大表查询效果更好",
                "summary": "MySQL 的连表查询我们经常使用，合理的使用连表查询会大大提升查询速度。MySQL使用的是一种叫做嵌套循环连接。",
                "tags": [
                    "mysql"
                ],
                "title": "MySQL连接查询原理",
                "viewTimes": 0
            },
            {
                "_id": 31,
                "category": "编程之路",
                "createTime": "2019-05-03T16:28:22",
                "markdownContent": "## 一、普通 MySQL 连接方法\n使用模块 MySQLdb 普通方式连接。\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nimport MySQLdb\nconn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='test')\ncursor = conn.cursor()\nsql_1 = \"select * from user where id = %s;\" % (5,)\nsql_2 = \"select * from user \\\n         where id = %s;\" % (5,)\nsql_3 = \"\"\"\n           insert into user(username, password)\n           values(\"yuchaoshui\", \"123\");\n        \"\"\"\ntry:\n    print cursor.execute(sql_1)\n    print cursor.fetchall()\n    print cursor.execute(sql_2)\n    print cursor.fetchall()\n    print cursor.execute(sql_3)\n    conn.commit()\nexcept Exception as e:\n    print(e)\n    conn.rollback()\ncursor.close()\nconn.close()\n```\n execute() 返回结果表示影响的行数。cursor.fetchone() 取回一条结果。sql_1 直接一行写完，sql_2 换行写完， sql_3 多行写。 查询时不需要 commit() 操作，插入、更新、删除时需要 commit() 提交。 \n\n\n## 二、使用连接池连接MySQL\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nimport MySQLdb\nfrom DBUtils.PooledDB import PooledDB\npool = PooledDB(MySQLdb, 5, host='127.0.0.1', port=3306, user='root', passwd='123', db='test')\nconn = pool.connection()\ncursor = conn.cursor()\nsql_1 = \"select * from user where id = %s;\" % (5,)\nsql_2 = \"select * from user \\\n         where id = %s;\" % (5,)\nsql_3 = \"\"\"\n           insert into user(username, password)\n           values(\"yuchaoshui\", \"123\");\n        \"\"\"\ntry:\n    print cursor.execute(sql_1)\n    print cursor.fetchall()\n    print cursor.execute(sql_2)\n    print cursor.fetchall()\n    print cursor.execute(sql_3)\n    conn.commit()\nexcept Exception as e:\n    print(e)\n    conn.rollback()\ncursor.close()\nconn.close()\n```\n5 为连接池里的最少连接数， 以后每次需要数据库连接就是用connection()函数获取连接就好了 \n\n\nPooledDB 的默认值\n```\nPooledDB(self, creator, mincached=0, maxcached=0, maxshared=0, maxconnections=0, blocking=False, maxusage=None, setsession=None, reset=True, failures=None, ping=1, *args, **kwargs)\n```\nPooledDB的参数： \nmincached，最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接\nmaxcached，最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接\nmaxconnections，最大的连接数，\nblocking，当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，直到当前连接数小于最大连接数，如果这个值是False，会报错，\nmaxshared , 当连接数达到这个数，新请求的连接会分享已经分配出去的连接 \n\n## 三、模块导入连接 MySQL\n  以连接池的方式，编写模块 mysqlhelper.py，可以在项目的其他地方导入MySQL连接实例即可使用。 模块点此下载\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nfrom __future__ import print_function\nfrom DBUtils.PooledDB import PooledDB\nimport MySQLdb\nimport sys\n__all__ = ['m'] + [\"m\"+str(i) for i in range(2, 11)]\nclass MH(object):\n    def __init__(self):\n        try:\n            print(\"Connecting MySQL Server {0}@{1}:{2} ..\".format(\n                self.__class__.db, self.__class__.host, self.__class__.port), end='.')\n            self.conn = self.__class__.pool.connection()\n            self.cursor = self.conn.cursor()\n            print(' ok!')\n        except Exception, e:\n            print(\"pool.connection error: {0}\".format(e))\n    def select(self, query=''):\n        try:\n            self.effect = self.cursor.execute(query)\n            return self.cursor\n        except Exception as e:\n            print(\"select error: {0}\".format(e))\n    def update(self, query=''):\n        try:\n            self.effect = self.cursor.execute(query)\n            self.conn.commit()\n        except Exception as e:\n            print(\"update error: {0}\".format(e))\n            self.conn.rollback()\n            self.effect = 0\n# M2 类继承自 M1，表示一个新的 MySQL 连接池。\n# 如果需要新的连接池 ，按照如下格式新增即可。\nclass MH2(MH):\n    pass\ndef init_pool(M,\n            host='127.0.0.1', \n            port=3306, \n            user='root', \n            password='', \n            database='test',\n            pool_size=5): \n    M.host = host\n    M.port = int(port)\n    M.user = user\n    M.password = password\n    M.db = database\n    M.pool_size = pool_size\n    try:\n        M.pool = PooledDB(MySQLdb, \n            M.pool_size,\n            host=M.host,\n            port=M.port,\n            user=M.user,\n            passwd=M.password,\n            db=M.db)\n    except Exception, e:\n        print(\"PooledDB init error: {0}\".format(e))\n        exit(1)\n# 初始化连接池，可以有多个。第一个参数是前面手动定义的连接池类。\ninit_pool(MH, '127.0.0.1', 3306, 'root', '123', 'test')\ninit_pool(MH2, '12.55.5.61', 3306, 'root', '123', 'test')\n# 定义将要被导出的MySQL实例。 一个连接池可同时提供多个实例对象。\nm = MH()\nm2 = MH2()\nif __name__ == \"__main__\":\n    pass\n    #print \"\\nm info:\"\n    #print m.select(\"select * from user;\").fetchone()\n    #print m.effect\n    #print m.select(\"select * from user;\").fetchall()\n    #print m.effect\n    #m.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    #print m.effect\n    ##################################################\n    #print \"\\nm2 info:\"\n    #print m2.select(\"select * from user;\").fetchone()\n    #print m2.effect\n    #print m2.select(\"select * from user;\").fetchall()\n    #print m2.effect\n    #m2.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    #print m2.effect\n```\n\n使用方法\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nfrom mysqlhelper import m, m2\nimport time\ndef test():\n    print \"\\nm info:\"\n    print m.select(\"select * from user;\").fetchone()\n    print m.effect\n    print m.select(\"select * from user;\").fetchall()\n    print m.effect\n    m.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    print m.effect\n    #################################################\n    print \"\\nm2 info:\"\n    print m2.select(\"select * from user;\").fetchone()\n    print m2.effect\n    print m2.select(\"select * from user;\").fetchall()\n    print m2.effect\n    m2.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    print m2.effect\nif __name__ == '__main__':\n    test()\n```",
                "summary": "Python 连接 MySQL的三种方式",
                "tags": [
                    "mysql",
                    "python"
                ],
                "title": "Python 连接 MySQL",
                "viewTimes": 0
            }
        ]
    },
    "err": "SUCCESS",
    "msg": ""
}
```
### Get Detail of Article
Endpoint:
```
GET:/api/v1/article/<int:id>
```
Example Response:
```
{
    "data": {
        "_id": 31,
        "category": "<blog.models.categories.Category object at 0x7fa4aa740208>",
        "createTime": "2019-05-03T16:28:22",
        "markdownContent": "## 一、普通 MySQL 连接方法\n使用模块 MySQLdb 普通方式连接。\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nimport MySQLdb\nconn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='test')\ncursor = conn.cursor()\nsql_1 = \"select * from user where id = %s;\" % (5,)\nsql_2 = \"select * from user \\\n         where id = %s;\" % (5,)\nsql_3 = \"\"\"\n           insert into user(username, password)\n           values(\"yuchaoshui\", \"123\");\n        \"\"\"\ntry:\n    print cursor.execute(sql_1)\n    print cursor.fetchall()\n    print cursor.execute(sql_2)\n    print cursor.fetchall()\n    print cursor.execute(sql_3)\n    conn.commit()\nexcept Exception as e:\n    print(e)\n    conn.rollback()\ncursor.close()\nconn.close()\n```\n execute() 返回结果表示影响的行数。cursor.fetchone() 取回一条结果。sql_1 直接一行写完，sql_2 换行写完， sql_3 多行写。 查询时不需要 commit() 操作，插入、更新、删除时需要 commit() 提交。 \n\n\n## 二、使用连接池连接MySQL\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nimport MySQLdb\nfrom DBUtils.PooledDB import PooledDB\npool = PooledDB(MySQLdb, 5, host='127.0.0.1', port=3306, user='root', passwd='123', db='test')\nconn = pool.connection()\ncursor = conn.cursor()\nsql_1 = \"select * from user where id = %s;\" % (5,)\nsql_2 = \"select * from user \\\n         where id = %s;\" % (5,)\nsql_3 = \"\"\"\n           insert into user(username, password)\n           values(\"yuchaoshui\", \"123\");\n        \"\"\"\ntry:\n    print cursor.execute(sql_1)\n    print cursor.fetchall()\n    print cursor.execute(sql_2)\n    print cursor.fetchall()\n    print cursor.execute(sql_3)\n    conn.commit()\nexcept Exception as e:\n    print(e)\n    conn.rollback()\ncursor.close()\nconn.close()\n```\n5 为连接池里的最少连接数， 以后每次需要数据库连接就是用connection()函数获取连接就好了 \n\n\nPooledDB 的默认值\n```\nPooledDB(self, creator, mincached=0, maxcached=0, maxshared=0, maxconnections=0, blocking=False, maxusage=None, setsession=None, reset=True, failures=None, ping=1, *args, **kwargs)\n```\nPooledDB的参数： \nmincached，最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接\nmaxcached，最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接\nmaxconnections，最大的连接数，\nblocking，当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，直到当前连接数小于最大连接数，如果这个值是False，会报错，\nmaxshared , 当连接数达到这个数，新请求的连接会分享已经分配出去的连接 \n\n## 三、模块导入连接 MySQL\n  以连接池的方式，编写模块 mysqlhelper.py，可以在项目的其他地方导入MySQL连接实例即可使用。 模块点此下载\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nfrom __future__ import print_function\nfrom DBUtils.PooledDB import PooledDB\nimport MySQLdb\nimport sys\n__all__ = ['m'] + [\"m\"+str(i) for i in range(2, 11)]\nclass MH(object):\n    def __init__(self):\n        try:\n            print(\"Connecting MySQL Server {0}@{1}:{2} ..\".format(\n                self.__class__.db, self.__class__.host, self.__class__.port), end='.')\n            self.conn = self.__class__.pool.connection()\n            self.cursor = self.conn.cursor()\n            print(' ok!')\n        except Exception, e:\n            print(\"pool.connection error: {0}\".format(e))\n    def select(self, query=''):\n        try:\n            self.effect = self.cursor.execute(query)\n            return self.cursor\n        except Exception as e:\n            print(\"select error: {0}\".format(e))\n    def update(self, query=''):\n        try:\n            self.effect = self.cursor.execute(query)\n            self.conn.commit()\n        except Exception as e:\n            print(\"update error: {0}\".format(e))\n            self.conn.rollback()\n            self.effect = 0\n# M2 类继承自 M1，表示一个新的 MySQL 连接池。\n# 如果需要新的连接池 ，按照如下格式新增即可。\nclass MH2(MH):\n    pass\ndef init_pool(M,\n            host='127.0.0.1', \n            port=3306, \n            user='root', \n            password='', \n            database='test',\n            pool_size=5): \n    M.host = host\n    M.port = int(port)\n    M.user = user\n    M.password = password\n    M.db = database\n    M.pool_size = pool_size\n    try:\n        M.pool = PooledDB(MySQLdb, \n            M.pool_size,\n            host=M.host,\n            port=M.port,\n            user=M.user,\n            passwd=M.password,\n            db=M.db)\n    except Exception, e:\n        print(\"PooledDB init error: {0}\".format(e))\n        exit(1)\n# 初始化连接池，可以有多个。第一个参数是前面手动定义的连接池类。\ninit_pool(MH, '127.0.0.1', 3306, 'root', '123', 'test')\ninit_pool(MH2, '12.55.5.61', 3306, 'root', '123', 'test')\n# 定义将要被导出的MySQL实例。 一个连接池可同时提供多个实例对象。\nm = MH()\nm2 = MH2()\nif __name__ == \"__main__\":\n    pass\n    #print \"\\nm info:\"\n    #print m.select(\"select * from user;\").fetchone()\n    #print m.effect\n    #print m.select(\"select * from user;\").fetchall()\n    #print m.effect\n    #m.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    #print m.effect\n    ##################################################\n    #print \"\\nm2 info:\"\n    #print m2.select(\"select * from user;\").fetchone()\n    #print m2.effect\n    #print m2.select(\"select * from user;\").fetchall()\n    #print m2.effect\n    #m2.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    #print m2.effect\n```\n\n使用方法\n```\n#!/usr/bin/env python\n# _*_ coding:utf-8 _*_\nfrom mysqlhelper import m, m2\nimport time\ndef test():\n    print \"\\nm info:\"\n    print m.select(\"select * from user;\").fetchone()\n    print m.effect\n    print m.select(\"select * from user;\").fetchall()\n    print m.effect\n    m.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    print m.effect\n    #################################################\n    print \"\\nm2 info:\"\n    print m2.select(\"select * from user;\").fetchone()\n    print m2.effect\n    print m2.select(\"select * from user;\").fetchall()\n    print m2.effect\n    m2.update(\"insert into user(username,password) values('haha', 'heihei');\")\n    print m2.effect\nif __name__ == '__main__':\n    test()\n```",
        "summary": "Python 连接 MySQL的三种方式",
        "tags": [
            "mysql",
            "python"
        ],
        "title": "Python 连接 MySQL",
        "viewTimes": 0
    },
    "err": "SUCCESS",
    "msg": ""
}
```
### archiving
Endpoint:
```
GET:/api/v1/articles/archiving/<string:nickname>
```
Example Response:
```
{
    "data": {
        "archivingList": [
            [
                {
                    "_id": 33,
                    "createTime": "2019-05-06T12:25:49",
                    "title": "Linux 提供简单 http server"
                },
                {
                    "_id": 28,
                    "createTime": "2019-05-03T16:28:22",
                    "title": "MySQL连接查询原理"
                },
                {
                    "_id": 29,
                    "createTime": "2019-05-03T16:28:22",
                    "title": "Redis安装及常用配置"
                },
                {
                    "_id": 30,
                    "createTime": "2019-05-03T16:28:22",
                    "title": "Ubuntu 时间设置"
                }
            ],
            [
                {
                    "_id": 31,
                    "createTime": "2019-04-03T16:28:22",
                    "title": "Python 连接 MySQL"
                }
            ]
        ]
    },
    "err": "SUCCESS",
    "msg": ""
}
```

more details please read the Makefile.



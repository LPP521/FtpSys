# -*- coding: utf-8 -*-   @Time    : 18-1-25 下午4:46
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

from conf.settings import *
import configparser
from os.path import join
import os


class User(object):
    """类属性,替代全局变量"""
    login_status = 0
    download_dir = ''
    upload_dir = ''
    allowed_storage = 0
    username = ''


def register():
    """新用户注册"""
    print('注册中'.center(20, '-'))
    # 1. 读取数据库信息
    config = configparser.ConfigParser()
    config.read(CONF_DIR)

    while True:
        # 2. 输入用户名
        username = input('用户名>>> ').strip()
        if username in config.sections():
            print('\033[1;35m 对不起,该用户名已经被注册 \033[0m', end='\n\n')
        else:
            if len(username) < 3:
                print('用户名长度至少是三位')
            else:
                while True:
                    # 3. 输入密码
                    password = input('密码>>> ').strip()
                    if len(password) <6:
                        print('\033[1;35m 输入至少为6位数 \033[0m')
                    else:
                        # 4. 输入申请的免费空间
                        storage = input('您申请的空间大小>>> ')
                        if storage.isdigit():
                            if int(storage) in range(20, 1000):
                                # 5. 存储用户注册信息
                                config.add_section(username)
                                config.set(username, 'password', password)
                                config.set(username, 'download_dir', USER_DOWNLOAD_TEMPLATE % username)
                                config.set(username, 'upload_dir', USER_UPLOAD_TEMPLATE % username)
                                config.set(username, 'storage',  storage)
                                config.set(username, 'lock_status',  '0')
                                with open(CONF_DIR, 'w') as f:
                                    config.write(f)
                                # 创建下载和上传文件夹
                                os.makedirs(join(BASE_DIR, USER_DOWNLOAD_TEMPLATE % username))
                                os.makedirs(join(BASE_DIR, USER_UPLOAD_TEMPLATE % username))
                                print('注册成功'.center(20, '-'))
                                input()
                                return


def login(func):
    """闭包函数"""
    def inner(**kwargs):
        if User.login_status:
            return func(username=User.username,download_dir=User.download_dir,
                        upload_dir=User.upload_dir, allowed_storage=User.allowed_storage)
        while True:
            choice = input('1.登录\n2.注册\n3.退出\n输入操作编号>>> ').strip()
            if choice == '1':
                # 1. 读取数据库信息
                config = configparser.ConfigParser()
                config.read(CONF_DIR)
                print()
                print('登录中'.center(20, '-'))
                while True:
                    # 2. 输入用户名
                    username = input('用户名>>> ').strip()
                    if username not in config.sections():
                        print('对不起,用户名输入有误', end='\n\n')

                    else:
                        # 3. 检测对应用户是否被锁定
                        lock_status = config[username]['lock_status']
                        if lock_status != '0':
                            print('\033[1;35m 对不起,该用户已被冻结 \033[0m', end='\n\n')

                        else:
                            count = 0
                            while count < 3:
                                # 4. 输入密码
                                password = input('密码>>> ').strip()
                                if password == config[username]['password']:
                                    # 5. 获取对应的用户信息,主要是获取用户下载路径和上传路径的绝对地址等
                                    User.download_dir = join(BASE_DIR, config[username]['download_dir'])
                                    User.upload_dir = join(BASE_DIR, config[username]['upload_dir'])
                                    User.allowed_storage = int(config[username]['storage']) * 1024 * 1024
                                    User.username = username
                                    # 6. 确保用户端有对应的上传和下载文件夹存在
                                    if not os.path.exists(join(BASE_DIR, USER_DOWNLOAD_TEMPLATE % username)):
                                        os.makedirs(join(BASE_DIR, USER_DOWNLOAD_TEMPLATE % username))
                                    if not os.path.exists(join(BASE_DIR, USER_UPLOAD_TEMPLATE % username)):
                                        os.makedirs(join(BASE_DIR, USER_UPLOAD_TEMPLATE % username))

                                    print('登录成功'.center(20, '-'))
                                    return func(username=User.username, download_dir=User.download_dir,
                                                upload_dir=User.upload_dir, allowed_storage=User.allowed_storage)

                                count += 1

                            if count == 3:
                                # 密码输入次数过多则直接锁定!
                                config.set(username, 'lock_status', '1')
                                with open(CONF_DIR, 'w') as f:
                                    config.write(f)
                                    print('\033[1;35m 对不起,您输入的密码次数过多, 已被锁定! \033[0m', end='\n\n')

            if choice == '2':
                register()

            if choice == '3':
                exit('退出')

    return inner



















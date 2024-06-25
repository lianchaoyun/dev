import ctypes
import inspect
from peewee import *
import datetime
from datetime import date
import time
import ctypes
import hashlib
import inspect
import os
import sys
import time
import calendar
from bs4 import BeautifulSoup
import importlib
from lib.eventbus import eventbus, subscriber
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from transitions import Machine
from time import sleep
import logging
"""
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
class SuperLove(subscriber, object):
    states = ['init', 'run', "process", 'stop']
    eb = eventbus()

    def __init__(self, name):
        self.name = name
        self.ctptq = None
        self.isTradeTime = True
        self.kittens_rescued = 0
        self.machine = Machine(model=self, states=SuperLove.states, initial='init')
        self.machine.add_transition(trigger='tg_init', source='init', dest='run', before='bf_init')
        self.machine.add_transition(trigger='tg_stop', source='*', dest='stop')
        self.machine.add_transition(trigger='tg_run', source='run', dest='process')
        self.eb.register_consumer(self, 'main')

    def process(self, eventobj):
        topic = eventobj.get_topic()
        data = eventobj.get_data()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "-", "main process:", data)

    def task_trade_time(self):
        now = datetime.now()
        ts = now.strftime("%Y-%m-%d %H:%M:%S")
        self.isTradeTime = True if now.minute == 55 else False
        print("开市任务:", ts)

    def task_test2(self):
        now = datetime.now()
        ts = now.strftime("%Y-%m-%d %H:%M:%S")
        print("测试任务2:", ts)

    def init_trade(self):
        if self.isTradeTime == True and self.ctptq is not None and self.ctptq.isRun == True:
            print("关闭交易端")
            self.ctptq.isRun = False
            self.ctptq = None
            sleep(38)

        if self.ctptq is None or self.ctptq.isRun == False:
            print("启动交易端")
            # importlib.reload(this)

    def bf_init(self):
        print("init successful")
        trigger_futures = OrTrigger(
            [
                CronTrigger(day_of_week="mon-fri", hour=8, minute=55),
                CronTrigger(day_of_week="mon-fri", hour=11, minute=31),
                CronTrigger(day_of_week="mon-fri", hour=12, minute=55),
                CronTrigger(day_of_week="mon-fri", hour=15, minute=1),
                CronTrigger(day_of_week="mon-fri", hour=20, minute=55),
                CronTrigger(day_of_week="tue-sat", hour=2, minute=31),
            ]
        )
        scheduler = BlockingScheduler()
        scheduler.remove_all_jobs()
        scheduler.add_job(func=self.task_trade_time, trigger=trigger_futures, id='task_trade_time')
        scheduler.add_job(func=self.task_test2, trigger=AndTrigger([CronTrigger(second=0), ]), id='task_test2')
        scheduler.add_job(func=self.init_trade, trigger='interval', seconds=120 * 60, id='init_trade')
        scheduler.start()

# 关闭线程
def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    print("close thread", tid, exctype, tid, res)
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

"""

# db = SqliteDatabase('loli.db')
db = MySQLDatabase('wuzhen', user='root', password='423522', host='127.0.0.1', port=3306)
db.connect()

class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    username = CharField(unique=True)
    nickname = CharField(null=True)
    birthday = DateField(null=True)
    name = CharField(null=True)
    email = CharField(null=True)
    status = IntegerField(null=True, default=0)
    avatar = CharField(null=True)
    url = CharField(null=True)
    email_verified_at = DateTimeField(null=True)
    password = CharField(null=True, default="123456")
    remember_token = CharField(null=True)
    create_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'users'


class TermRelationships(BaseModel):
    object_id = BigIntegerField(default=0)
    term_taxonomy_id = BigIntegerField(default=0)
    term_order = IntegerField(default=0)

    class Meta:
        db_table = 'term_relationships'


class Options(BaseModel):
    option_id = BigIntegerField(default=0, primary_key=True)
    option_name = CharField(null=True, default="")
    option_value = CharField(null=True, default="")
    autoload = CharField(null=True, default="")
    group = CharField(null=True, default="")
    desc = CharField(null=True, default="")

    class Meta:
        db_table = 'options'


class Posts(BaseModel):
    ID = BigIntegerField(unique=True)
    post_author = BigIntegerField(default=0)
    post_date = DateTimeField(default=datetime.datetime.now)
    post_date_gmt = DateTimeField(default=datetime.datetime.utcnow())
    post_content = TextField()
    post_title = TextField()
    post_excerpt = TextField(default="")
    post_status = CharField(default="publish")
    comment_status = CharField(default="open")
    ping_status = CharField(default="open")
    post_password = CharField(default="")
    post_name = CharField(default="")
    to_ping = TextField(default="")
    pinged = TextField(default="")
    post_modified = DateTimeField(default=datetime.datetime.now)
    post_modified_gmt = DateTimeField(default=datetime.datetime.utcnow())
    post_content_filtered = TextField(default="")
    post_parent = BigIntegerField(default=0)
    guid = CharField(default="")
    menu_order = IntegerField(default=0)
    post_type = CharField(default="post")
    post_mime_type = CharField(default="")
    comment_count = BigIntegerField(default=0)

    class Meta:
        db_table = 'posts'


class Assets(BaseModel):
    id = BigIntegerField(default=0, primary_key=True)
    url = CharField(null=True, default="")
    type = CharField(null=True, default="")
    hash = CharField(null=True, default="")
    title = CharField(null=True, default="")
    group = CharField(null=True, default="")
    create_date = DateTimeField(default=datetime.datetime.utcnow())
    update_time = DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        db_table = 'assets'


# 时间格式化 格式:23:59:59   参数: 2000-12-31 24:59:59   或者  0
def ts2time(ts):
    if isinstance(ts, str):
        if len(ts) > 19:
            ts = ts[0:19]
        return time.strftime("%H:%M:%S", time.strptime(ts, "%Y-%m-%d %H:%M:%S"))

    if len(str(ts)) < 10:
        return "00:00:00"
    return time.strftime("%H:%M:%S", time.localtime(int(str(int(ts))[0:10])))


# 时间转时间戳 参数:int
def ts2timestamp(ts):
    if len(str(ts)) > 10:
        return int(str(int(ts))[0:10])
    return ts


# 格式化float,一位小数
def fmt_float(f):
    return int(f) if f - int(f) == 0 else float('{:.1f}'.format(f))


def clean_attrs(tag):
    tag.attrs = None
    for e in tag.findAll("img"):
        for attribute in e.attrs:
            if attribute in ["onclick"]:
                del e[attribute]
                print("成功删除属性")
                break
    return tag


# 日志打印
def log(*args):
    timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(timestr + "  " + str(args))


# 获取当前时间
def getNow():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 获取当前日期
def getNowDay():
    return time.strftime("%Y%m%d", time.localtime())


# 获取当前时间戳
def getNowTimestamp():
    return calendar.timegm(time.gmtime())


# 获取文件扩展名，dot是否不包含.
def file_extension(path, dot=False):
    if dot:
        return os.path.splitext(path)[1]
    return os.path.splitext(path)[1][1:]


# 获取文件hash
def file2hash(file_path, Bytes=1024):
    md5_1 = hashlib.md5()  # 创建一个md5算法对象
    with open(file_path, 'rb') as f:  # 打开一个文件，必须是'rb'模式打开
        while 1:
            data = f.read(Bytes)  # 由于是一个文件，每次只读取固定字节
            if data:  # 当读取内容不为空时对读取内容进行update
                md5_1.update(data)
            else:  # 当整个文件读完之后停止update
                break
    ret = md5_1.hexdigest()  # 获取这个文件的MD5值
    return ret


# 获取字符串md5
def string2md5(originstr):
    b = bytes(originstr, encoding="utf8")
    signaturemd5 = hashlib.md5()
    signaturemd5.update(b)
    return signaturemd5.hexdigest()


# 比较两个文件是否相等
def compare_file(f1, f2):
    # 显示文件信息
    st1 = os.stat(f1)
    st2 = os.stat(f2)
    # 比较文件大小
    if st1.st_size != st2.st_size:
        return False
    bufsize = 8 * 1024
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize)  # 读取指定大小的数据进行比较
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True


# 遍历当前目录
def fileList():
    dir = os.getcwd()
    # 遍历所有文件，包括子目录
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            # 获取目录的名称
            print(dir)
            # 获取目录的路径
            print(os.path.join(root, dir))
    # 遍历所有文件，不包括子目录
    for root, dirs, files in os.walk(os.getcwd()):
        print(root)


# 字典转数据库更新语句
def dict2uupdatesql(item):
    return ",".join(["%s='%s'" % (k, v) for k, v in item.items() if v is not None])


# 字典转数据库插入语句
def dict2insertsql(item, table_name):
    ls = [(k, v) for k, v in item.items() if v is not None]
    # print(' %s (' % table_name + ','.join([i[0] for i in ls]) + ')')
    sql = 'INSERT INTO %s (' % table_name + ','.join([i[0] for i in ls]) + ') VALUES (' + ','.join(
        repr(i[1]) for i in ls) + ');'
    # print(sql)
    return sql


# 重命名文件
def renameFiles(folder_path):
    index = 1
    for path, dirs, files in os.walk(folder_path):
        for name in files:
            file_path = os.path.join(path, name)
            new_filepath = os.path.join(path, str(index) + str(os.path.splitext(file_path)[-1]))
            print(file_path + " => " + new_filepath)
            os.rename(file_path, new_filepath)
            index += 1


'''
def create1(ID, term_taxonomy_id, post_author, post_content, post_title):
    try:
        with db.atomic() as tx:
            print("开始发布")
            p_ID = Posts.create(post_author=post_author, post_content=post_content, post_title=post_title)
            TermRelationships.create(ID=ID, object_id=p_ID, term_taxonomy_id=term_taxonomy_id)
            print(str(p_ID) + " => 文章ID 发布成功")
        return True
    except Exception as err:
        print(err)
        return False

def testYoyo21():
    ID = 1
    term_taxonomy_id = 1
    post_author = 1
    post_title = "2！"
    post_content = "美好的站长生活从这里开始！"
    rs = create1(ID=ID, term_taxonomy_id=term_taxonomy_id, post_author=post_author, post_content=post_content,
                post_title=post_title)
'''


# 处理数据库数据
def process_db_data():
    for i in range(1, 6000):
        try:
            print(i)
            p = Posts.get(Posts.ID == i)
            if p:
                # soup = BeautifulSoup(p.post_content, 'html.parser')
                # soup = clean_attrs(soup)
                # cc = Posts.update(post_content=str(soup)).where(Posts.ID == i).execute()
                print(p.post_title)
            else:
                print("none")
        except Exception as err:
            print(err)
    print("===========完成============")


def process_data_db_assets(dir):
    dir = dir if dir else "C:\project\data"
    for root, dirs, files in os.walk(dir):
        for file in files:
            realPath = os.path.join(root, file)
            hash = file2hash(realPath)
            type = file_extension(realPath)
            if type in ["jpg","jpeg","png","gif","webp"]:
                type="image"
            elif type in ["mp4"]:
                type = "video"
            row = Assets.get_or_none(Assets.hash == hash)
            try:
                with db.atomic() as tx:
                    if  row:
                        r = Assets.update(url=realPath[len(dir):], type=type).where(Assets.hash == hash).execute()
                    else:
                        r = Assets.create(url=realPath[len(dir):], type=type, hash=hash)
                    print(realPath, hash, r)

            except Exception as err:
                print(err)


if __name__ == '__main__a':
    #zhenzhen(
    pass

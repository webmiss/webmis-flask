import time,random
from math import floor
from config.env import Env
from library.redis import Redis
from util.util import Util
from model.model import Model

# 数据类
class Data:

  # 机器标识
  machineId: int = Env.machine_id
  max8bit: int = 8     #随机数位数
  max10bit: int = 10   #机器位数
  max12bit: int = 12   #序列数位数

  # 分区时间
  partition: dict = {
    'p2208': 1661961600,
    'p2209': 1664553600,
    'plast': 1664553600,
  }

  # 薄雾算法
  def Mist(redisName: str):
    # 自增ID
    redis = Redis()
    autoId = redis.Incr(redisName)
    redis.Close()
    # 随机数
    randA = random.randint(0,255)
    randB = random.randint(0,255)
    # 位运算
    mist = int((autoId << (Data.max8bit + Data.max8bit)) | (randA << Data.max8bit) | randB)
    return mist

  # 雪花算法
  def Snowflake():
    # 时间戳
    t = int(round(time.time() * 1000))
    # 随机数
    rand = random.randint(0,4095)
    # 位运算
    mist = int((t << (Data.max10bit + Data.max12bit)) | (Data.machineId << Data.max12bit) | rand)
    return mist

  # 图片地址
  def Img(img: str):
    return Env.base_url+img if img!='' else ''

  # 分区-获取ID
  # p2209 = Data.PartitionID('2022-10-01 00:00:00', 'logs')
  def PartitionID(date: str, table: str, column: str='ctime'):
    t = Util.Time()
    m = Model()
    m.Table(table)
    m.Columns('id', column)
    m.Where(column+' < %s', t)
    m.Order(column+' DESC, id DESC')
    one = m.FindFirst()
    one['date'] = date
    one['time'] = t
    return one

  # 分区-获取名称
  # Data().PartitionName(1661961600, 1664553600)
  def PartitionName(self, stime: int, etime: int):
    p1 = self.__getPartitionTime(stime)
    p2 = self.__getPartitionTime(etime)
    arr = []
    start = False
    for k in self.partition.keys() :
      if k==p1 : start=True
      if start : arr += [k]
      if k==p2 : break
    return Util.Implode(',', arr)
  # 获取名称
  def __getPartitionTime(self, time: int):
    name: str = ''
    for k,v in self.partition.items() :
      if(time<v) : return k
      name = k
    return name

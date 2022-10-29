from task.base import Base
from library.redis import Redis
from service.logs import Logs as LogsService
from util.util import Util

# 日志
class Logs(Base):

  # 首页
  def Main(self):
    while True :
      redis = Redis()
      data = redis.BLPop('logs', 10)
      redis.Close()
      if not data : continue
      # 保存
      msg = data[1]
      res = self._logsWrite(msg)
      if not res :
        LogsService.File('upload/erp/Logs.json', Util.JsonEncode(msg))

  # 写入
  def _logsWrite(self, msg):
    # 数据
    data = Util.JsonDecode(msg)
    self.Print(data)
    return True

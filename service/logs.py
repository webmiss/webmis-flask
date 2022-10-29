from config.env import Env
from library.file_eo import FileEo
from library.redis import Redis
from util.util import Util

# 日志
class Logs:

  # 文件
  def File(file: str, content: str):
    FileEo.Root = Env.root_dir
    FileEo.WriterEnd(file, content+"\n")

  # 生产者
  def Logs(data: dict):
    redis = Redis()
    redis.RPush('logs', Util.JsonEncode(data))
    redis.Close()

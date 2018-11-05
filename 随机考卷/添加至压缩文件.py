import zipfile
import os
import logging

# 日志
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
# 关闭日志
# logging.disable(logging.CRITICAL)
# 写日志
logging.debug("开始测试")
# 加载压缩文件
exampleZip = zipfile.ZipFile("随机考卷.zip", "w")
# 写日志
logging.debug(os.listdir("随机考卷"))
# 写日志
logging.debug("循环 - 随机考卷中的列表")
# 循环 考卷文件数量
for i in os.listdir("随机考卷"):
    # 添加至压缩文件
    exampleZip.write("随机考卷/%s" % i, compress_type=zipfile.ZIP_DEFLATED)
    # 写日志
    logging.debug("当前文件名: %s" % i)
# 输出提示
print(exampleZip.namelist())
# 关闭文件
exampleZip.close()
# 写日志
logging.debug("循环结束")

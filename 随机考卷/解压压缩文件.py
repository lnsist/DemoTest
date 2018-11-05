import zipfile

# 加载压缩文件
exampleZip = zipfile.ZipFile('随机考卷.zip')
# 解压至指定文件夹
exampleZip.extractall("解压-随机考卷")
# 关闭
exampleZip.close()

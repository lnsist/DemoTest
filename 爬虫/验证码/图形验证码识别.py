"""
    识别普通图形验证码
date: 18-10-7 下午7:05
"""
import tesserocr
from PIL import Image

# 打开图形验证码
# image_open = Image.open("a.jpg")  # 验证码空心字无法识别
image_open = Image.open("图形验证码.jpg")
# 加载识别
result = tesserocr.image_to_text(image_open)
# 同上
# result = tesserocr.file_to_text("图形验证码.jpg")

# 输出结果
print("进行图片处理前的识别:", result)

# 结果偏差大, 需要处理一下图片

# 将图片转为灰度图像
image_open_copy = image_open.convert("L")
# 展示图片
# image_open_copy.show()
# 二值化处理 -- 设置默认阀值
image_open_copy = image_open.convert("1")
# 展示图片
# image_open_copy.show()

# 完整处理步骤

# 转为灰度图像
image_open = image_open.convert("L")
# 二值化阀值
threshold = 120
# 像素点, 二值化处理, 总共 256 个亮度, 设置相应二值化阀值
table = []
# 循环 256 个亮度
for i in range(256):
    # 小于阀值, 不取值, 否则取值
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
# 图片像素点操作 -- 每个点进行提亮, 去除干扰线, table -- 每个像素点的操作, 1 -- 输出模式
image_open = image_open.point(table, "1")
# 展示图片
image_open.show()
# 加载识别
result = tesserocr.image_to_text(image_open)
# 输出结果
print("进行图片处理后的识别", result)

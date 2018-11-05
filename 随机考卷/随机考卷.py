"""
创建 35 份不同的测验试卷。
• 为每份试卷创建 50 个多重选择题，次序随机。
• 为每个问题提供一个正确答案和 3 个随机的错误答案，次序随机。
• 将测验试卷写到 35 个文本文件中。
• 将答案写到 35 个文本文件中。
这意味着代码需要做下面的事：
• 将州和它们的首府保存在一个字典中。
• 针对测验文本文件和答案文本文件，调用 open()、 write()和 close()。
• 利用 random.shuffle()随机调整问题和多重选项的次序。
"""
import random

# 问题和答案
capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix', 'Arkansas': 'Little Rock',
            'California': 'Sacramento', 'Colorado': 'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover',
            'Florida': 'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise',
            'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas': 'Topeka',
            'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine': 'Augusta', 'Maryland': 'Annapolis',
            'Massachusetts': 'Boston', 'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson',
            'Missouri': 'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City',
            'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'Mexico': 'Santa Fe', 'New York': 'Albany',
            'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
            'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence', 'South Carolina': 'Columbia',
            'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City',
            'Vermont': 'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'WestVirginia': 'Charleston',
            'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

# 35 份考卷
for i in range(35):
    # 打开 考试 文件
    q_fil = open("随机考卷\考卷%d.txt" % (i + 1), "w", encoding="utf-8")
    # 打开 答案 文件
    as_file = open("随机考卷\考卷%d答案.txt" % (i + 1), "w", encoding="utf-8")

    # 首行, 姓名: 日期: 学号
    q_fil.write('姓名:\n\n日期:\n\n学号:\n\n')
    # 第二行, 书卷名称
    q_fil.write((' ' * 20) + '各州首府问卷 (Form %s)' % (i + 1))
    # 换行
    q_fil.write('\n\n')
    # 获取所有 "问题" key
    states = list(capitals.keys())
    # 打乱顺序
    random.shuffle(states)
    # 50 道题目
    for j in range(50):
        # 获取正确答案 states[j] key
        correct_as = capitals[states[j]]
        # 错误答案 列表
        error_as = list(capitals.values())
        # 删除错误答案中的 正确答案
        del error_as[error_as.index(correct_as)]
        # 在错误答案中  随机获取 3 个
        error_as = random.sample(error_as, 3)
        # 问题的答案选项 = 错误答案 +  正确答案
        answerOptions = error_as + [correct_as]
        # 打乱顺序, 不至于所有正确答案都在最后
        random.shuffle(answerOptions)
        # 写问题在考卷上
        q_fil.write(("%s. 这个%s州的首府是: " % (str(j + 1).rjust(2, "0"), states[j])).ljust(30, " "))
        # 4 个选项
        for k in range(4):
            # ABCD 对应 选项
            q_fil.write("\t%s. %s" % ("ABCD"[k], str(answerOptions[k]).ljust(15, " ")))
        # 换行
        q_fil.write("\n")
        # 考卷答案 - 写入正确答案选项
        as_file.write("%s. %s%s" % (str(j + 1).rjust(2, "0"), "ABCD"[answerOptions.index(correct_as)], "\n" if (j + 1) % 10 == 0 else "\t"))

    # 写完 50 个问题再关闭文件
    q_fil.close()
    # 关闭文件
    as_file.close()

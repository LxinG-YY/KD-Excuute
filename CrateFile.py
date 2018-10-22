import codecs

code_start = 2273
code_num = 10
for i in range(code_num):
    code = '00' + str(code_start + i)
    for j in range(20):
        index = '%02d' % (j + 1)
        filename = "E:/Project/KD/outsource/news_source/" + "source" + "_" + code + "_" + str(index) + ".txt"
        # print(filename)
        with codecs.open(filename, 'w+', 'utf-8'):
            pass

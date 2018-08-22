import codecs

start_code = 600051
code_num = 4
num = 0
for i in range(code_num):
    code = str(start_code + i)
    for j in range(20):
        index = "%02d" % (j + 1)
        # filename1 = "targetH" + "_" + code + "_" + str(index) + ".txt"
        # address1 = "E:/Project/KD/news_target/" + filename1
        filename2 = "split" + "_" + code + "_" + str(index) + ".txt"
        address2 = "E:/Project/KD/news_split/" + filename2
        # print(address)
        with codecs.open(address2, 'r+', 'utf-8') as f:
            s2 = f.read()
        if s2[0:4] == 'feff':
            s2[:] = s2[6:]
        with codecs.open(address2, 'w+', 'utf-8') as f:
            f.write(s2)
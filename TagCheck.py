import codecs
start_code = 600055
code_num = 5
num = 0
for i in range(code_num):
    code = str(start_code + i)
    for j in range(20):
        index = "%02d" % (j + 1)
        filename1 = "targetH" + "_" + code + "_" + str(index) + ".txt"
        address1 = "E:/Project/KD/news_target/" + filename1
        filename2 = "split" + "_" + code + "_" + str(index) + ".txt"
        address2 = "E:/Project/KD/news_split/" + filename2
        # print(address)
        with codecs.open(address1, 'r+', 'utf-8') as f:
            s1 = f.read()
        a1 = s1.split()
        with codecs.open(address2, 'r+', 'utf-8') as f:
            s2 = f.read()
        a2 = s2.split()
        for i in range(len(a2)):
            if a2[i] == 'B-ORG-0'or a2[i] == 'I-ORG-0':
                print(num+1, ": ","ZeroMisoperation: on ", str(i+1))
        if len(a1) != len(a2):
            num = num + 1
            print(num, ': ', filename1, ': ', len(a1), " AND ", filename2, ': ', len(a2))

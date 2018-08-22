import codecs
start_code = 600051
code_num = 4
num = 20
start_index = 1
# =====================
FLAG_source = 0
FLAG_split = 1
FLAG_target = 1
# =====================
for i in range(code_num):
    code = str(start_code + i)
    for j in range(num):
        index = "%02d" % (j + start_index)
        filename1 = "targetH" + "_" + code + "_" + str(index) + ".txt"
        address1 = "E:\\Project\\KD\\news_target\\" + filename1
        filename2 = "source" + "_" + code + "_" + str(index) + ".txt"
        address2 = "E:\\Project\\KD\\news_source\\" + filename2
        filename3 = "split" + "_" + code + "_" + str(index) + ".txt"
        address3 = "E:\\Project\\KD\\news_split\\" + filename3
        # filename2 = "split" + "_" + code + "_" + str(index) + ".txt"
        # address2 = "E:/Project/KD/news_split/" + filename2
        # print(address)
        if FLAG_source:
            with codecs.open(address2, 'r+', 'utf-8') as f:
                s1 = f.read()
            # s1 = 'Flag ' + s1
            a1 = s1.split()
            if a1 != []:
                if a1[0][0] == '\ufeff':
                    print('Find \ufeff at', address2)
                    a1[0] = a1[0][1:len(a1[0])]
                s = ''.join(a1)
                with codecs.open(address2, 'w+', 'utf-8') as f:
                    f.write(s)
        if FLAG_split:
            with codecs.open(address3, 'r+', 'utf-8') as f:
                s1 = f.read()
            # s1 = 'Flag ' + s1
            a1 = s1.split()
            if a1 != []:
                if a1[0][0] == '\ufeff':
                    print('Find \ufeff at', address3)
                    a1[0] = a1[0][1:len(a1[0])]
                s = ' '.join(a1)
                with codecs.open(address3, 'w+', 'utf-8') as f:
                    f.write(s)

        if FLAG_target:
            with codecs.open(address1, 'r+', 'utf-8') as f:
                s1 = f.read()
            # s1 = 'Flag ' + s1
            a1 = s1.split()
            if a1 != []:
                if a1[0][0] == '\ufeff':
                    print('Find \ufeff at', address1)
                    a1[0] = a1[0][1:len(a1[0])]
                s = ' '.join(a1)
                with codecs.open(address1, 'w+', 'utf-8') as f:
                    f.write(s)





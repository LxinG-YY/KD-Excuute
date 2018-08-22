import codecs
start_code = 600051
code_num = 4
for i in range(code_num):
    code = str(start_code + i)
    for j in range(20):
        index = "%02d" % (j + 1)
        address = "E:/Project/KD/news_target/" + "targetH" + "_" + code + "_" + str(index) + ".txt"
        # print(address)

        with codecs.open(address, 'r+', 'utf-8-sig') as f:
            s = f.read()
        a = s.split()
        for i in range(len(a)):
            if a[i] == 'B-ORG-A' or a[i] == 'B-ORG-O' or a[i] == 'I-ORG-A' or a[i] == 'I-ORG-O' or a[i] == '<feff>':
                continue
            a[i] = 'O'
        s = ''
        for i in range(len(a)):
            if i == 0:
                s = s + a[i]
                continue
            s = s + ' ' + a[i]
        with codecs.open(address, 'w+', 'utf-8-sig') as f:
            f.write(s)






















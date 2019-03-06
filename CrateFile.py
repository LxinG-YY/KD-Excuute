import codecs

<<<<<<< HEAD
code_start = 2263
=======
code_start = 2273
>>>>>>> 0d1d8bae1de118278b0690fb90517cb33dbbb1b0
code_num = 10
for i in range(code_num):
    code = '00' + str(code_start + i)
    for j in range(20):
        index = '%02d' % (j + 1)
<<<<<<< HEAD
        filename = "E:/KD/outsource/news_source/" + "source" + "_" + code + "_" + str(index) + ".txt"

=======
        filename = "E:/Project/KD/outsource/news_source/" + "source" + "_" + code + "_" + str(index) + ".txt"
        # print(filename)
>>>>>>> 0d1d8bae1de118278b0690fb90517cb33dbbb1b0
        with codecs.open(filename, 'w+', 'utf-8'):
            pass

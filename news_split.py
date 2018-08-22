import ternary.common.utils as utils
import os
import re

"""
news_split(stock_start_index, stock_num, news_num, source_folder, output_folder, target_folder):
    将源文件source_folder中的新闻（每个txt文件对应一个新闻，每支股票有对应的20篇新闻，新闻文件名按照股票代码升序排列）读取，
    进行分词（包括去停用词和金融分词）。将每条新闻的分词结果存入output_folder和target_folder路径对应的新闻文件（txt文件）中
    
Parameters
----------
stock_start_index:int
    待处理的股票新闻中，第一支股票的股票代码，如：处理关于股票600151,600152,600153...的新闻，stock_start_index = 600151
stock_num:int
    每次要处理多少股票的新闻
news_num:int
    每只股票对应的新闻数量
source_folder:string
    源文件夹的全限定名（源文件夹存储股票新闻）
output_folder:string
    分词结果存储路径（全限定名）
target_folder:
    标注文件存储路径（全限定名）
"""


def news_split(stock_start_index, stock_num, news_num, source_folder, output_folder, target_folder):

    if source_folder[-1] != '/':
        source_folder += '/'
    if output_folder[-1] != '/':
        output_folder += '/'
    if target_folder[-1] != '/':
        target_folder += '/'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for i in range(stock_num):
        tmp = stock_start_index + i
        
        for j in range(news_num):
            index = "%02d" % (j + 1)
            input_filename = "source_" + str(tmp) + "_" + str(index) + ".txt"
            output_filename = "split_" + str(tmp) + "_" + str(index) + ".txt"
            target_filename = "targetH_" + str(tmp) + "_" + str(index) + ".txt"

            if os.path.exists(source_folder + input_filename):
                f_src = open(source_folder + input_filename, mode="r", encoding='utf-8')
                f_output = open(output_folder + output_filename, encoding='utf-8', mode="w")
                f_target = open(target_folder + target_filename, encoding='utf-8', mode="w")

                line = f_src.read()
                line = re.sub('\s+', '', line)
                line_seg = utils.kd_cut(line, False)

                s = " ".join(line_seg)
                f_output.write(s)
                f_target.write(s)

                f_output.close()
                f_target.close()
                f_src.close()


stock_start_index = 300426
stock_num = 10
news_num = 20
source_folder = 'E:/Project/KD/outsource/news_source'
output_folder = 'E:/Project/KD/outsource/news_split'
target_folder = 'E:/Project/KD/outsource/news_target'
news_split(stock_start_index, stock_num, news_num, source_folder, output_folder, target_folder)
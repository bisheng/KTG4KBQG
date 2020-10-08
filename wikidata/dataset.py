# -*- coding: utf-8 -*-
import re


class SimpleQuestionDS:
    def __init__(self, fb2w, free_path, wiki_path):
        self.fb2w = fb2w
        self.free_path = free_path
        self.wiki_path = wiki_path

    # 构建freebase和wikidata映射的dict的数组
    def create_map(self):
        map = []
        for line in self.fb2w.readlines():
            line = re.sub(' .\n', '', line)
            list = line.split("\t")
            source = re.findall(r"(?<=/m.).*(?=>)", list[0])

            dict = {}
            dict['free'] = source[0]
            dict['wiki'] = list[2]
            map.append(dict)
        return map

    # 根据映射将freebase数据转换成wikidata数据，并写入新的数据文本文件中
    def produce(self, map):
        count = 0
        for line in self.free_path.readlines():
            list = line.split("\t")
            source = re.findall(r"(?<=/m/).*", list[0])
            target = re.findall(r"(?<=/m/).*", list[2])
            flag_s = 0
            flag_o = 0
            for i in map:
                if source[0] == i['free']:
                    line = line.replace(list[0], i['wiki'])
                    # print(i['wiki'])
                    flag_s = 1
                elif target[0] == i['free']:
                    line = line.replace(list[2], i['wiki'])
                    # print(i['wiki'])
                    flag_o = 1
                # 如果这条数据的subject和object都被替换成wikidata的数据，则保留
                if flag_s == 1 and flag_o == 1:
                    self.wiki_path.write(line)
                    count = count + 1
                    print(count)
                    break


"""
# 处理freebase到wikidata的映射文件
fb2w = open('fb2w.nt', 'r', encoding='utf8')
f = open('./SimpleQuestions/valid.txt', 'r', encoding='utf8')
f2 = open('./SimpleQuestions/valid_new.txt', 'w', encoding='utf8')

simple_question = SimpleQuestionDS(fb2w, f, f2)
map = simple_question.create_map()
simple_question.produce(map)
"""

import math
import time

import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torchtext import data
from torchtext.data import Iterator, BucketIterator
import torch.nn.functional as F


class Dataset(data.Dataset):
    name = "lic2019"

    @staticmethod
    def sort_key(ex):
        return len(ex.text)

    def __init__(self, path, label_field, desc_field, class_field, **kwargs):
        fields = [("label", label_field), ("desc", desc_field), ("class", class_field)]
        examples = []
        print('loading dataset from {}'.format(path))
        with open(path, encoding="utf-8") as f:
            # special
            for line in f.readlines():
                if "######" in line:
                    line.replace("######", "### ###")
                label = line.split("###")[1]
                desc = line.split("###")[2]
                cla = line.split("###")[3].replace("\n", "")
                print([label, desc, cla])
                examples.append(data.Example.fromlist([label, desc, cla], fields=fields))

        print('size of dataset in {} is : {}'.format(path, len(examples)))
        super(Dataset, self).__init__(examples, fields, **kwargs)


# 增加初始token和结尾token
BOS_WORD = "<sos>"
EOS_WORD = "<eos>"
BLANK_WORD = "<blank>"
MAX_LEN = 30

Label = data.Field(init_token=BOS_WORD, eos_token=EOS_WORD, lower=True)
Desc = data.Field(init_token=BOS_WORD, eos_token=EOS_WORD, lower=True)
Class = data.Field(init_token=BOS_WORD, eos_token=EOS_WORD, lower=True)

# train_path = "entity_info_test.txt"
valid_path = "wikidata_desc_cate_valid.txt"
valid_path = "wikidata_desc_cate_valid.txt"
valid_path = "wikidata_desc_cate_valid.txt"
# test_path = "./SimpleQuestions/entity_info_test.txt"
# train_data = Dataset(train_path, src_field=SRC, trg_field=TRG)
valid_data = Dataset(valid_path, label_field=Label, desc_field=Desc, class_field=Class)
# test_data = Dataset(test_path, label_field=Label, desc_field=Desc,class_field=Class)

Label.build_vocab(valid_data, min_freq=2)  # 建立词汇表的时候需要把valid，test的单词都加进去吗？ yes
Desc.build_vocab(valid_data, min_freq=2)
Class.build_vocab(valid_data, min_freq=2)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

BATCH_SIZE = 128

valid_iterator = data.Iterator(
    dataset=valid_data,
    batch_size=BATCH_SIZE,
    device=device, sort_key=lambda x: (len(x.label), len(x.desc), len(x.cla)))


def get_embedding(iterator):
    for i, batch in enumerate(iterator):

        print(batch.label)
        break
        # label = batch.label
        # desc = batch.desc
        # clas = batch.cla
        #
        # print(label)
        # print(desc)
        # print(clas)


get_embedding(valid_iterator)



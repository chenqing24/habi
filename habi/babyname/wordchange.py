# coding=gbk
import os

'''
遍历的字典
'''
print(os.path.abspath('.'))

dict_zi = {}
set_zi = []


def dict2list(dic:dict):
    '''
    将字典转化为列表
    :param dic:
    :return:
    '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst


with open(os.path.abspath('.') + '\\4s5j_v2.txt', 'r', encoding='utf-8') as f:
    # print(f.read())
    for x in f.read():
        # print(x)
        # print(ord(x))
        x_ord = ord(x)
        if x_ord and (x_ord not in dict_zi):
            if 19968 <= x_ord <= 51863:
                dict_zi[x_ord] = x

    # print(sorted(dict2list(dict_zi), key=lambda x:x[0], reverse=False))
    i = 0
    for char in sorted(dict2list(dict_zi), key=lambda x:x[0], reverse=False):
        i += 1
        # if i<10:
        #     print(str(ord(char[1])) + " " + char[1])
        set_zi.append(char[1])

    print(set_zi)
    print(len(set_zi))


import os

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


with open(os.path.abspath('.') + '\\3500zi.txt', 'r') as f:
    # print(f.read())
    for x in f.read():
        # print(x)
        # print(ord(x))
        x_ord = ord(x)
        if x_ord and (x_ord not in dict_zi):
            if 12299 < x_ord <= 40863:
                dict_zi[x_ord] = x

    # print(sorted(dict2list(dict_zi), key=lambda x:x[0], reverse=False))
    for char in sorted(dict2list(dict_zi), key=lambda x:x[0], reverse=False):
        set_zi.append(char[1])

    print(set_zi)
    print(len(set_zi))

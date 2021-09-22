"""
@author:Wang Xinsheng
@File:parsetime.py
@description:...
@time:2021-08-16 18:06
"""
import re

test_datetime = '他的生日是2016年12-12 14:34,是个可爱的小宝贝.二宝的生日是2016-12-21 11:34,好可爱的.'

s = '2021年05月20日05:21 | 来源：'
# date
def get_time(s):
    # mat = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2})",s)
    mat = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)",s)
    if mat:
        time = mat.groups()[0]
    else:
        time = ''
    return time

# ('2016-12-12',)
if __name__ == '__main__':
    pass
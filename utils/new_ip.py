# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/10/5  13:50'



def generate_new_ip(str):
    seg_list = str.split('.')
    seg_new = []
    for i in range(0,4):
        seg = seg_list[i]
        pos = len(seg)-1
        seg = seg[:pos] + '*' + seg[pos+1:]
        seg_new.append(seg)
    return ('.').join(seg_new)

if __name__ == "__main__":
    print generate_new_ip('123.12.243.222')

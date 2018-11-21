# coding=utf-8

import requests
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

#登录
serverIp = '192.168.10.67'
login_url = "http://%s/login.php" %serverIp
login_values = {'user_name': 'admin',
                'password': 'pProbejy'}
session = requests.session()
session.post(login_url, data=login_values)
#要添加的ip组
src_ips = [{"data[ip_group_name]": "内部ip组",
            "data[group_ips]": "58.215.115.165/32",
            "data[user_ids][]": "5b399e38747350bc4365e623"},
           {"data[ip_group_name]": "内部ip组1",
            "data[group_ips]": "188.166.155.144/32",
            "data[user_ids][]": "5b399e38747350bc4365e623"}]

dst_ips = [{"data[ip_group_name]": "外部ip组",
            "data[group_ips]": "192.168.1.254/32;172.16.10.251/32",
            "data[user_ids][]": "5b399e38747350bc4365e623"}]


    # 增加源ip组：
def addsrc_ipgroup():
    addsrc_url = "http://%s/ip_group.php?action=addnew&type=src" %serverIp
    a = 0
    for i in range(len(src_ips)):
        session.post(addsrc_url, data=src_ips[i])
        a += 1
    print 'Set  %d srcip groups successfully!' %a
    #增加目的ip组
def adddst_ipgroup():
    adddst_url = "http://%s/ip_group.php?action=addnew&type=dst" % serverIp
    for i in range(len(dst_ips)):
        session.post(adddst_url, data=dst_ips[i])
    print 'Set dstip groups successfully!'






if __name__=='__main__':
    addsrc_ipgroup()
    adddst_ipgroup()









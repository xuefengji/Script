# coding=utf-8

import os, time

result = os.popen('service pprobe status').readlines()
def uninstalliProbe():
    os.system('pkill -9 monit')
    os.system('service pprobe stop')
    os.system('service pprobe unload_driver')
    os.system('rm -rf /home/juyun')
    os.system('rm -rf /opt/iProbe')
    os.system('rm -rf /etc/init.d/pprobe')
    os.system('rm -rf /etc/init/monit.conf')
    os.system('rm -rf /var/spool/mail/juyun')
    os.system('userdel juyun')


def installdcheck(path):
    if len(result) == 21:
        uninstalliProbe()
        #安装驱动
        os.system('cd')
        os.system('cd driver_10g/driver/')
        os.system('make')
        os.system('make install')
        os.system('python /lib/modules/2.6.32-573.el6.x86_64/kernel/drivers/net/ps_ixgbe/install.py  4 4')
        #一键安装基础包
        os.system('cd /home/jxf/dcheck/release/inin')
        os.system('sh -x install.sh ')
        print '拷贝准备好的nfsen.ini文件和pprobe.cfg文件到/opt/dcheck/etc下,确保pprobe.cfg中bus_list以及cpu绑核与安装机器一致'
        time.sleep(60)
        #安装dcheck安装包
        os.chdir(path)
        os.system('./update.sh')
    elif len(result) == 16:
        os.chdir(path)
        os.system('./update.sh')





if __name__=='__main__':
    path = '/home/jxf/GHW/update_0712/'
    installdcheck(path)




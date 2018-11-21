# coding=utf-8

import os

result = os.popen('service pprobe status').readlines()

#卸载dcheck
def uninstalldcheck():
    os.system('wget http://192.168.10.77:8080/dcheckinstall/uninstall.sh; sh -x uninstall.sh ')

#编译并安装
def checkiProbe(path):
    os.chdir(path)
    if len(result) == 16:     #判断是否安装dchecktou
        uninstalldcheck()
        # path = path+'/iprobe4xx'
        os.system("./buildall.sh --debug=no --cputype=native --buildtype=fresh --nicspeed=10G")
    elif len(result) == 0:
            os.system("./buildall.sh --debug=no --cputype=native --buildtype=fresh --nicspeed=10G")
    #编译
    else:
        os.system("./buildall.sh --debug=no --cputype=native --buildtype=upgrade --nicspeed=10G")
    # time.sleep(900)
    #安装(获取最新编译的文件)
    files = os.listdir(path)
    files.sort(key=lambda fn: os.path.getmtime(path + "/" + fn))
    file_new = files[-1]
    os.system('./' + file_new)

if __name__=='__main__':
    path = '/home/jxf/iprobe4xx'
    checkiProbe(path)
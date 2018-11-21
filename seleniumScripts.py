# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
import configparser
import sys

import sys
reload(sys)
sys.setdefaultencoding('utf-8')



browser = webdriver.Chrome()
# browser = webdriver.Firefox()

#登录三清云系统
def login(uname, passw, team):
    login_url = 'http://www.yunmonitor.cn/sign_in'
    team_url = 'http://www.yunmonitor.cn/launchpad'
    browser.get(login_url)
    time.sleep(5)
    # browser.quit() 输入用户名
    username = browser.find_element_by_xpath('//*[@id="userName"]')
    username.clear()
    username.send_keys(uname)
    #输入密码
    password = browser.find_element_by_css_selector('form.form-signin input[placeholder="密码"]')
    password.clear()
    password.send_keys(passw)
    browser.find_element_by_css_selector('form.form-signin a[class*=submit] span').click()
    time.sleep(5)
    current_url = browser.current_url
    if current_url == team_url:
        print u'登录成功'
        browser.find_element_by_css_selector('ul.org-list>li[title="%s"]' % team).click() #可以选择要进入的团队
        time.sleep(5)
        # return browser.current_url
        # lis = browser.find_element_by_class_name('text-ellipsis')
        # print len(lis)
        # if len(lis) == 0:
        #     print u'请创建团队'
        #     browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/ul/li[3]/a').click()
        #     time.sleep(10)
        #     team_name = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/form/div/div/div[1]/input')
        #     team_name.send_keys('testing')
        #     browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/button[2]/span').click()
        #     time.sleep(10)
        #     browser.find_element_by_class_name('text-ellipsis').click()
        #     time.sleep(10)

    else:
        print u'账号或密码错误'
        browser.close()
        browser.quit()


#切换角色（个人或团队）
def change(role):
        home = browser.find_element_by_css_selector('div.el-submenu__title>label[class="text-ellipsis"]')
        ActionChains(browser).move_to_element(home).perform()
        time.sleep(10)
        browser.find_element_by_css_selector('ul.el-menu>li>span[title=%s]' % role).click()
        # WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(role))
        # browser.find_element_by_css_selector('ul.el-menu>li>span[title="个人"]').click()
        time.sleep(10)


#创建文件夹
def create_folder(foldername):
    browser.find_element_by_xpath('//span[text()="仪表盘列表"]/following-sibling::span//i').click()
    # add_button.click()
    time.sleep(5)
    #创建文件夹
    browser.find_element_by_xpath('//li[text()="创建文件夹"]').click()
    time.sleep(5)
    folder_name = browser.find_element_by_xpath('//label[text()="文件夹名称"]/following-sibling::div//input')
    folder_name.clear()
    folder_name.send_keys(foldername)
    browser.find_element_by_xpath('//span[text()="创建文件夹"]/../following-sibling::div[2]//button[2]').click()
    time.sleep(5)


    # print len(browser.find_elements_by_class_name('text'))


def create_dashboards(folderName, dict):
    browser.find_element_by_xpath('//span[text()="仪表盘列表"]/following-sibling::span//i').click()
    # add_button.click()
    time.sleep(5)
    browser.find_element_by_xpath('//li[text()="创建仪表盘"]').click()
    time.sleep(5)
    browser.find_element_by_css_selector('div.home input[placeholder="请选择"]').click()
    time.sleep(5)
    #选择文件夹
    # browser.find_elements_by_css_selector('ul.el-select-dropdown__list>li')[-1].click()
    browser.find_element_by_css_selector('ul.el-select-dropdown__list li[title="%s"]' % folderName).click()
    dash_name = browser.find_element_by_xpath('//label[text()="仪表盘名称"]/following-sibling::div//input')
    dash_name.clear()
    dash_name.send_keys(dict['dashboard_name'])
    browser.find_element_by_xpath('//span[text()="创建仪表盘"]/../following-sibling::div[2]//button[2]').click()
    time.sleep(5)



def add_zd(dict):
    browser.find_element_by_css_selector('span#step4 span').click()
    time.sleep(10)
    browser.find_element_by_xpath('//li[text()="添加计算字段"]').click()
    time.sleep(5)
    #新增字段名
    name = browser.find_element_by_css_selector('form.el-form input[placeholder="请输入字段名称"]')
    name.send_keys(dict['field_name'])
    time.sleep(3)
    #选择字段类型
    browser.find_element_by_css_selector('form.el-form input[placeholder="请选择字段类型"]').click()
    time.sleep(5)
    browser.find_element_by_xpath('//span[text()="%s"]' % dict['type']).click()
    time.sleep(5)
    # 输入计算表达式
    express = browser.find_element_by_css_selector('div#expression div[class="CodeMirror-lines"]')
    express.click()
    
    # browser.execute_script("arguments[0].focus();", express)
    # express.__setattr__("style", "visibility: visible;")
    # express.clear()
    express.send_keys({dict['expression']})
    time.sleep(3)
    browser.find_element_by_xpath('//span[text()="添加计算字段"]/../following-sibling::div[2]//button[2]').click()
    time.sleep(5)



def create_chart(dict):
    #添加图表
    add_button = browser.find_element_by_link_text('添加图表')
    add_button.click()
    time.sleep(5)
    #选择数据源
    browser.find_element_by_css_selector('input[placeholder="请选择数据分组"]').click()
    time.sleep(10)
    # ops = browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/ul')
    # op = ops.find_elements_by_tag_name('li')
    # op[3].click()
    browser.find_element_by_xpath('//span[text()="%s"]' % dict['data_group']).click()
    time.sleep(3)
    browser.find_element_by_xpath('//span[text()="新建图表"]/../following-sibling::div[2]//button[2]').click()
    time.sleep(5)
    #添加图表名
    chartname = browser.find_element_by_css_selector('div.chart-title input[placeholder="请输入标题"]')
    chartname.clear()
    chartname.send_keys(dict['chart_name'])
    #添加维度和指标字段:
       #1、获取字段名，拖拽维度：
    dimensions = dict['dimensions']
    zd_types = browser.find_elements_by_css_selector('ul#step3 span[class="item-text"]')
    zd_types_list = []
    for span in zd_types:
        zd_types_list.append(span.get_attribute("title"))
    for i in range(len(dimensions)):
        data_type = dimensions[i]['data_type']
        field_name = dimensions[i]['field_name']
        if data_type in zd_types_list:
            browser.find_element_by_css_selector('ul#step3 span[title="%s"]' % data_type).click()
            time.sleep(5)
            field_names = browser.find_elements_by_css_selector('ul#step3 span[title="%s"]~ul span' % data_type)
            field_name_list = []
            for span in field_names:
                field_name_list.append(span.get_attribute("title"))
            if field_name in field_name_list:
                wdz = browser.find_element_by_css_selector('ul#step3 li[class="tree-item"] span[title="%s"]' % field_name)
                print wdz.get_attribute("title")
                wdk = browser.find_element_by_css_selector('div#step1 div[class="dimension-args"]')
                print wdk.get_attribute("class")
                ActionChains(browser).drag_and_drop(wdz, wdk).perform()
                # ActionChains(browser).click_and_hold(wdz).move_to_element(wdk).release().perform()
                time.sleep(20)
            else:
                add_zd(dimensions[i])
                field_name_list.append(browser.find_elements_by_css_selector("div.menu-item span")[-1].get_attribute("title"))
                wdz = browser.find_element_by_css_selector('ul#step3 span[title="%s"]' % field_name)
                wdk = browser.find_element_by_css_selector('div#step1 div[class="dimension-args"]')
                ActionChains(browser).drag_and_drop(wdz, wdk).perform()
                time.sleep(20)

        else:
            add_zd(dimensions[i])
            zd_types_list.append(browser.find_elements_by_css_selector("div.menu-title span")[-1].get_attribute("title"))
            browser.find_element_by_css_selector('ul#step3 span[title="%s"]' % data_type).click()
            time.sleep(5)
            wdz = browser.find_element_by_css_selector('ul#step3 span[title="%s"]' % field_name)
            wdk = browser.find_element_by_css_selector('div#step1 div[class="dimension-args"]')
            # ActionChains(browser).drag_and_drop(wdz, wdk).perform()
            ActionChains(browser).click_and_hold(wdz)
            ActionChains(browser).move_to_element(wdk).release().perform()
            time.sleep(20)
    #2、获取字段名，拖拽指标
    metrics = dict['metrics']
    for j in range(len(metrics)):
        data_type = metrics[j]['data_type']
        field_name = metrics[j]['field_name']
        if data_type in zd_types_list:
            browser.find_element_by_css_selector('ul#step3 span[title="%s"]' % data_type).click()
            time.sleep(5)
            field_names = browser.find_elements_by_css_selector('ul#step3 span[title="%s"]~ul span' % data_type)
            field_name_list = []
            for span in field_names:
                field_name_list.append(span.get_attribute("title"))
            if field_name in field_name_list:
                zbz = browser.find_element_by_css_selector('ul#step3 span[title="%s"]' % field_name)
                print zbz.get_attribute("title")
                zbk = browser.find_element_by_css_selector('div#step2 div[class="metric-args"]')
                print zbk.get_attribute("class")
                ActionChains(browser).drag_and_drop(zbz, zbk).perform()
                # ActionChains(browser).click_and_hold(zbz)
                #
                # ActionChains(browser).move_to_element(zbk).release().perform()
                time.sleep(20)
            else:
                add_zd(metrics[j])
                field_name_list.append(browser.find_elements_by_css_selector("div.menu-item span")[-1].get_attribute("title"))
                zbz = browser.find_element_by_css_selector('ul#step3 span[title="%s"]' % field_name)
                zbk = browser.find_element_by_css_selector('div#step2 div[class="metric-args"]')
                ActionChains(browser).drag_and_drop(zbz, zbk).perform()
                # ActionChains(browser).click_and_hold(zbz)
                # ActionChains(browser).move_to_element(zbk).release().perform()
                time.sleep(20)
        else:
            add_zd(metrics[j])
            zd_types_list.append(browser.find_elements_by_css_selector("div.menu-title span")[-1].get_attribute("title"))
            browser.find_element_by_css_selector('ul#step3 span[title="%s"]' % data_type).click()
            time.sleep(5)
            zbz = browser.find_element_by_css_selector('ul#step3 span[title="%s"]' % field_name)
            zbk = browser.find_element_by_css_selector('div#step2 div[class="metric-args"]')
            ActionChains(browser).drag_and_drop(zbz, zbk).perform()
            # ActionChains(browser).click_and_hold(zbz)
            # ActionChains(browser).move_to_element(zbk).release().perform()
            time.sleep(20)
    #选择图表类型:
    browser.find_element_by_css_selector('#step6 > ul a[class*="%s"]' % dict['chart_type']).click()
    time.sleep(3)
    browser.find_element_by_xpath('//button[text()="后退"]').click()
    time.sleep(10)



def delete_folder(flag):
    #flag：0表示不删除 1表示删除
    if flag == 1:
        while True:
            folders = browser.find_elements_by_class_name('menu-title')
            if len(folders) != 0:
                ActionChains(browser).move_to_element(folders[0]).perform()
                browser.find_element_by_css_selector('div.btn-box>i[title="删除"]').click()
                time.sleep(3)
                browser.find_element_by_css_selector('div.el-message-box__btns>button:nth-child(2)').click()
                time.sleep(5)
            else:
                print "文件夹已全部删除"
                break


if __name__ == '__main__':
    uname = 'xuefeng.ji'
    passw = 'P@ssw0rd'
    team = 'Home'
    login(uname, passw, team)
    change("个人")
    #判断是否有folder
    is_folder = browser.find_elements_by_class_name('el-collapse-item')
    if len(is_folder) != 0:
        browser.find_elements_by_class_name('menu-title')[0].click()
        time.sleep(3)
        with open('create.json', 'r') as files:
            info = json.loads(files.read())
            for i in range(len(info)):
                folder_name = info[i]['folder_name']
                create_folder(folder_name)
                for j in range(len(info[i]['dashboards'])):
                    dashboard_name = info[i]['dashboards'][j]
                    create_dashboards(info[i]['folder_name'], dashboard_name)
                    browser.find_element_by_css_selector('div.menu-title span[title="%s"]' % info[i]['folder_name']).click()
                    time.sleep(3)
                    # dashboards = browser.find_element_by_css_selector('div.is-active>div:nth-child(2)').find_elements_by_class_name('el-collapse-item__content')
                    # dashboards[-1].click()
                    browser.find_element_by_css_selector('div.is-active div[title="%s"]' % dashboard_name['dashboard_name']).click()
                    time.sleep(3)
                    for k in range(len(info[i]['dashboards'][j]['charts'])):
                        chart_info = info[i]['dashboards'][j]['charts'][k]
                        create_chart(chart_info)
                # browser.find_element_by_css_selector('div.menu-title span[title="%s"]' % info[i]['folder_name']).click()
                time.sleep(5)
            delete_folder(0)
    else:
        with open('create.json', 'r') as files:
            info = json.loads(files.read())
            for i in range(len(info)):
                folder_name = info[i]['folder_name']
                create_folder(folder_name)
                for j in range(len(info[i]['dashboards'])):
                    dashboard_name = info[i]['dashboards'][j]
                    create_dashboards(info[i]['folder_name'], dashboard_name)
                    browser.find_element_by_css_selector('div.menu-title span[title="%s"]' % info[i]['folder_name']).click()
                    time.sleep(3)
                    browser.find_element_by_css_selector('div.is-active div[title="%s"]' % dashboard_name['dashboard_name']).click()
                    time.sleep(3)
                    for k in range(len(info[i]['dashboards'][j]['charts'])):
                        chart_info = info[i]['dashboards'][j]['charts'][k]
                        create_chart(chart_info)
            # browser.find_element_by_css_selector('div.menu-title span[title="%s"]' % info[i]['folder_name']).click()
            time.sleep(5)
            delete_folder(0)
    browser.close()
        # create_folder('qqqqqq')
        # create_dashboards("qqqqqq", 'tetetette')
        # browser.find_elements_by_class_name('menu-title')[-1].click()
        # dashboards = browser.find_element_by_css_selector('div.is-active>div:nth-child(2)').find_elements_by_class_name('el-collapse-item__content')
        # print len(dashboards)
        # dashboards[-1].click()
        # time.sleep(3)
        # create_chart("all data", 'aaaaaaa', "chart-C2")





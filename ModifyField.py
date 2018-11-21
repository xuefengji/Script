# coding=utf-8

import json
import ConfigParser
import requests
import copy
import time
import codecs


class modifyField():
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        with codecs.open('config.ini', 'r', encoding='utf-8') as f:
            cf.readfp(f)
        self.server = cf.get('server', 'host')
        self.login_info = {'username': cf.get('users', 'username'), 'password': cf.get('users', 'password')}
        self.org_name = cf.get('org', 'org_name')
        self.data_group = cf.get('data_group', 'data_group')
        self.modify_fields = cf.get('modify_fields', 'modify_fields')
        self.modify_payload = eval(cf.get('modify_payload', 'modify_payload'))
        # self.snmp = eval(cf.get('snmp', 'snmp'))


    #登录并获取guid
    def login(self):
        session = requests.session()
        html = session.post('http://%s/api/users/sign_in/' % self.server, data=self.login_info)
        html_dict = json.loads(html.content)
        if html_dict['result'] == 'success':
            orgs = html_dict['data']['orgs']
            for org in orgs:
                if self.org_name in org['org_name']:
                    org_guid = org['guid']
                    member_guid = org['member_guid']
                    # print org_guid
        return session, org_guid, member_guid

    #获取数据源的guid
    def get_data_group(self, session, org_guid):
        url = 'http://%s/api/orgs/%s/data_groups/' % (self.server, org_guid)
        # session = requests.session()
        html = session.get(url)
        html_dict = json.loads(html.content)
        if html_dict['result'] == 'success':
            data_group_list = html_dict['data']['data_groups']
            for data_group in data_group_list:
                if self.data_group == data_group['data_group_name']:
                    data_group_guid = data_group['guid']
                    # print data_group_guid
                    return data_group_guid



    #获取相应的基础字段,并修改名称
    def get_datagroup_field(self, session, org_guid, data_group_guid):
        url = 'http://%s/api/orgs/%s/data_groups/%s/fields/search/' % (self.server, org_guid, data_group_guid)
        data = {
            "data_group_guid": data_group_guid,
            "filters": [],
            "query_string": "*",
            "time_range": {
                "from": int(time.time() - 15*60) * 1000,
                "to": int(time.time() * 1000)
            }
        }
        html = session.post(url, json=data)
        html_dict = json.loads(html.content)
        # print url, json.dumps(data)
        # # print html_dict['result']
        # print html_dict
        if html_dict['result'] == 'success':
            fields_list = html_dict['data']['normal']
            # print fields_list
            # for modify_field in modify_fields
                # print snmp
            with open('snmp.json', 'r') as f:
                snmp = json.loads(f.read())
            for fields in fields_list:
                if self.modify_fields == fields['field_id']:
                    for field in fields['children']:
                        for key in snmp:
                            if field['field_name'] == key:
                                if 'children' in field:
                                    for item in field['children']:
                                        for key1 in snmp[key]['children']:
                                            if item['field_name'] == key1:
                                                item['field_name'] = snmp[key]['children'][key1]
                                    field['field_name'] = snmp[key][key]
                                else:
                                    field['field_name'] = snmp[key]
            return fields_list


    #修改相对应的字段名
    def modify_field(self,session, data_group_guid, fields_list):
        url = 'http://%s/api/orgs/%s/data_groups/%s/fields/modify/' % (self.server, org_guid, data_group_guid)
        # data = {"field_type":0,"field_name":"cpuUtilization11","field_id":"snmp.cpuUtilization","data_type":"long","agg_type":["dimension"]}
        # modify_fields = copy.deepcopy(self.modify_fields)
        data = copy.deepcopy(self.modify_payload)
        # for modify_field in modify_fields:
        for fields in fields_list:
            if self.modify_fields == fields['field_id']:
                for field in fields['children']:
                    if 'children' in field:
                        for item in field['children']:
                            data['field_name'] = item['field_name']
                            data['field_id'] = item['field_id']
                            data['data_type'] = item['data_type']
                            html = session.post(url, json=data)
                            html_dict = html.json()
                            if html_dict['result'] == 'success':
                                print '字段名修改成功'
                        data['field_name'] = field['field_name']
                        data['field_id'] = field['field_id']
                        data['data_type'] = field['data_type']
                        html = session.post(url, json=data)
                        html_dict = html.json()
                        if html_dict['result'] == 'success':
                            print '字段名修改成功'
                    else:
                        data['field_name'] = field['field_name']
                        data['field_id'] = field['field_id']
                        data['data_type'] = field['data_type']
                        html = session.post(url, json=data)
                        html_dict = html.json()
                        if html_dict['result'] == 'success':
                            print '字段名修改成功'






if __name__=='__main__':
    a = modifyField()
    modify_fields = copy.deepcopy(a.modify_fields)
    session, org_guid, memguid = a.login()
    # print guid, memguid
    data_group_guid = a.get_data_group(session, org_guid)
    fields_list = a.get_datagroup_field(session, org_guid, data_group_guid)
    # print fields_list
    a.modify_field(session, data_group_guid, fields_list)




















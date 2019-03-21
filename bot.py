#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import configparser
import json

# python git test

class TulingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.robot_switch = True

        try:
            cf = configparser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
        except Exception:
            pass
        print('tuling_key:', self.tuling_key)

    def tuling_auto_reply(self, uid, msg):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api/v2"
            user_id = uid.replace('@', '')[:30]
            headers = {'Content-Type': 'application/json'}
            body = {
                'reqType': 0,
                'perception': {
                    'inputText': {
                        'text': msg
                    }
                },
                'userInfo': {
                    'apiKey': self.tuling_key,
                    'userId': user_id
                }

            }
            r = requests.post(url, headers=headers, data=json.dumps(body))
            respond = json.loads(r.text)
            result = ''
            # 暂时只处理文本和url
            groupType = 0
            for res in respond['results']:
                if res['groupType'] == 0:
                    if res['resultType'] == 'text':
                        result = res['values']['text'].replace('<br>', '  ')
                    if res['resultType'] == 'url':
                        result = res['values']['url']
                else:
                    if groupType == 0:
                        groupType = res['groupType']
                    if res['groupType'] == groupType:
                        if res['resultType'] == 'text':
                            result = result + '\t' + \
                                res['values']['text'].replace('<br>', '  ')
                        if res['resultType'] == 'url':
                            result = result + '\t' + res['values']['url']

            print('    ROBOT:', result)
            return result
        else:
            return "知道啦"

    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = ['退下', '走开', '关闭', '关掉', '休息', '滚开']
        start_cmd = ['出来', '启动', '工作']
        if self.robot_switch:
            if msg_data in stop_cmd:
                self.robot_switch = False
                self.send_msg_by_uid('[Robot]' + '机器人已关闭！', msg['to_user_id'])
        else:
            if msg_data in start_cmd:
                self.robot_switch = True
                self.send_msg_by_uid('[Robot]' + '机器人已开启！', msg['to_user_id'])

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # 自己发送的文本信息，发送命令来开启或关闭机器人
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            self.send_msg_by_uid(self.tuling_auto_reply(
                msg['user']['id'], msg['content']['data']), msg['user']['id'])
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                '''detail元素类型为含有 type 与 value 字段的字典，
                 type 为字符串 str (表示元素为普通字符串，此时value为消息内容) 
                 或 at (表示元素为@信息， 此时value为所@的用户名)'''
                my_names = self.get_group_member_name(
                    msg['user']['id'], self.my_account['UserName'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:  # 如果@了我
                    src_name = msg['content']['user']['name']
                    reply = 'to ' + src_name + ': '
                    if msg['content']['type'] == 0:  # text message
                        reply += self.tuling_auto_reply(
                            msg['content']['user']['id'], msg['content']['desc'])
                    else:
                        reply += "对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])


def main():
    bot = TulingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()

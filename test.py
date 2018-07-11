#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *


class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            # return
            if msg['user']['name'] == u'惠学日语班主任ひかり小光老师':
                if u'n1' in msg['content']['data'].lower():
                    self.send_msg_by_uid(u'俺爱你！', msg['user']['id'])
                if u'n2' in msg['content']['data'].lower():
                    self.send_msg_by_uid(u'你好漂亮！', msg['user']['id'])
                if u'n3' in msg['content']['data'].lower():
                    self.send_msg_by_uid(u'你瘦了！', msg['user']['id'])
            #self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])


    # def schedule(self):
    #     self.send_msg(u'惠学日语班主任ひかり小光老师', u'俺爱你')
    #     time.sleep(1)



def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()

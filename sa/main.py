#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/04/2018 22:26
# @Author  : hades
# @Software: PyCharm
import hashlib
import json
import os
import socket
import struct
import sys
import threading
import time
import uuid

import rumps

reload(sys)
sys.setdefaultencoding("utf-8")


class FuckTheSupplicant(rumps.App):
    def __init__(self):
        super(FuckTheSupplicant, self).__init__('Supplicant', icon='icon.png')
        self.get_config()  # read config
        self.quit_button = rumps.MenuItem(u'下线 & 退出', key='q', callback=self.quit_application)
        self.status_menu = rumps.MenuItem(u'等待连接')
        self.reupnet_menu = rumps.MenuItem(u'掉线重连', callback=self.re_upnet)
        self.reupnet_menu.state = int(self.config['re-upset'])
        self.menu = [self.status_menu, None, rumps.MenuItem(u'上线', callback=self.click_upset, ), self.reupnet_menu,
                     None, u'偏好设置', u'反馈', None]
        # link flag
        self.status_flag = 0

    @rumps.clicked(u"上线", key='u')
    def click_upset(self, _):
        self.start_connect()

    def re_upnet(self, sender):
        sender.state = not sender.state
        self.re_upset = not self.re_upset
        self.save_config(sender.state)  # save re-upnet config

    @rumps.clicked(u"偏好设置")
    def click_setting(self, _):
        os.system('open config.fts')

    @rumps.clicked(u"反馈")
    def click_feedback(self, _):
        self.dialog("BUG REPORT:i@mayuko.cn")

    def quit_application(self):
        print 'quit'
        self.disconnect()
        rumps.quit_application()

    # get local mac address
    def get_mac_address(self):
        mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac_address[e:e + 2] for e in range(0, 11, 2)])

    # get remote host
    def get_host(self):
        host = '219.218.154.250'  # For YTU
        return host

    # get local ip
    def get_local_ip(self):
        try:
            csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            csock.connect(('8.8.8.8', 80))
            (addr, port) = csock.getsockname()
            csock.close()
            return addr
        except socket.error:
            return '127.0.0.1'

    # read config
    def get_config(self):
        try:
            js_config = ''
            for line in open("config.fts"):
                js_config = line
            self.config = json.loads(js_config)
            self.mac_address = self.config['mac_address']
            self.host = self.config['host']
            self.number = self.config['number']
            self.password = self.config['password']
            self.re_upset = self.config['re-upset']

        except IOError:
            print u"config not exist!"
            self.send_notice(u'请在config.fts中填写配置信息')
            self.config = {
                'host': self.get_host(),
                'mac_address': self.get_mac_address(),
                'number': '',
                'password': '',
                're-upset': True,
                'version': '0.1.1',
                'bug_report': 'i@mayuko.cn'
            }
            js_config = json.dumps(self.config)
            file_object = open('config.fts', 'w')
            file_object.write(js_config)
            file_object.close()

    # save config
    def save_config(self, status):
        status = True if (int(status) == 1) else False
        self.config['re-upset'] = status
        js_config = json.dumps(self.config)
        file_object = open('config.fts', 'w')
        file_object.write(js_config)
        file_object.close()

    # notcie
    def send_notice(self, content):
        pass
        rumps.notification("Fuck The Supplicant", "", content)

    # connect
    def start_connect(self):
        print "try upset"
        self.status_flag = 0
        self.local_ip = self.get_local_ip()
        print "local ip is " + self.local_ip
        self.t_link = threading.Thread(target=self.creat_process, )
        self.t_link.start()

    # creat a thread
    def creat_process(self):
        self.connect()

    # try connect
    def connect(self):
        print u"try connect"
        self.status_menu.title = u"正在连接"
        self.link_attempts = 0
        self.index = 0x01000000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)
        while self.link_attempts < 8 and int(self.status_flag) != 1 and int(self.status_flag) != -1:
            try:
                upnet_packet = self.generate_upnet(self.mac_address, self.local_ip, self.number, self.password)
                session = self.upnet(self.sock, upnet_packet)
                self.breathe(self.sock, self.mac_address, self.local_ip, session, self.index)
            except Exception, e:
                print u"link_attempts is " + str(self.link_attempts)
                self.status_menu.title = u"重新连接"
                self.link_attempts = self.link_attempts + 1
                print u"try connect again"
        self.status_menu.title = u"连接超时"
        print u"time out"

    # downnet
    def disconnect(self):
        self.status_flag = 0
        downnet_packet = self.generate_downnet(self.mac_address, self.local_ip, self.session, self.index)
        self.send(self.sock, downnet_packet)
        self.sock.close()
        self.t_link.join(0)  # delete thread
        print u"down net success"

    # show notcie
    def dialog(self, msg):
        rumps.alert(msg)

    # print log
    def print_console(self, msg):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file_log = open('applog.log', 'a+')
        file_log.write(now_time + msg + "\n")
        file_log.close()

    # send sock
    def send(self, sock, packet):
        host = self.host
        port = 3848
        sock.sendto(packet, (host, port))

    # sock connect
    def upnet(self, sock, packet):
        self.send(sock, packet)
        upnet_ret = sock.recv(3848)
        upnet_ret = [i for i in struct.unpack('B' * len(upnet_ret), upnet_ret)]
        self.decrypt(upnet_ret)
        session_len = upnet_ret[22]
        session = upnet_ret[23:session_len + 23]
        self.session = session
        message_len = upnet_ret[upnet_ret.index(11, 35) + 1]
        message = upnet_ret[upnet_ret.index(11, 35) + 2:message_len + upnet_ret.index(11, 35) + 2]
        message = ''.join([struct.pack('B', i) for i in message]).decode('gbk')
        print message
        if 0 == int(upnet_ret[20]):
            self.status_flag = -1
            print u"connect fail"
            self.status_menu.title = u"验证错误"
            self.send_notice(u'密码或MAC地址绑定错误')
        else:
            self.status_flag = 1
            print u"connect success"
            self.status_menu.title = u"已连接"
            self.send_notice(u'连接成功')
            return session

    # keep breathe
    def breathe(self, sock, mac_address, local_ip, session, index):
        time.sleep(0)
        while True and int(self.status_flag) == 1:
            print u"keep online"
            breathe_packet = self.generate_breathe(mac_address, local_ip, session, index)
            self.send(sock, breathe_packet)
            try:
                breathe_ret = sock.recv(3848)
            except socket.timeout:
                continue
            else:
                status = struct.unpack('B' * len(breathe_ret), breathe_ret)
                if status[20] == 0:
                    print u"keep connect fail"
                    self.status_flag = 0
                    self.send_notice(u'opps！网络已断开')
                    self.status_menu.title = u"已掉线"
                    if self.re_upset:
                        print u"re upset"
                        self.t_link.join(0)
                        self.t_link = threading.Thread(target=self.creat_process,
                                                       args=(self.mac_address, self.local_ip, self.host, self.number,
                                                             self.password,))
                        self.t_link.start()
                    else:
                        self.status_menu.title = u"重连失败"
                        self.send_notice(u'尝试重新连接失败')
                index += 3

    # encrypt
    def encrypt(self, buffer):
        for i in range(len(buffer)):
            buffer[i] = (buffer[i] & 0x80) >> 6 | (buffer[i] & 0x40) >> 4 | (buffer[i] & 0x20) >> 2 | (
                                                                                                          buffer[
                                                                                                              i] & 0x10) << 2 | (
                                                                                                                                    buffer[
                                                                                                                                        i] & 0x08) << 2 | (
                                                                                                                                                              buffer[
                                                                                                                                                                  i] & 0x04) << 2 | (
                                                                                                                                                                                        buffer[
                                                                                                                                                                                            i] & 0x02) >> 1 | (
                                                                                                                                                                                                                  buffer[
                                                                                                                                                                                                                      i] & 0x01) << 7

    # decrypt
    def decrypt(self, buffer):
        for i in range(len(buffer)):
            buffer[i] = (buffer[i] & 0x80) >> 7 | (buffer[i] & 0x40) >> 2 | (buffer[i] & 0x20) >> 2 | (
                                                                                                          buffer[
                                                                                                              i] & 0x10) >> 2 | (
                                                                                                                                    buffer[
                                                                                                                                        i] & 0x08) << 2 | (
                                                                                                                                                              buffer[
                                                                                                                                                                  i] & 0x04) << 4 | (
                                                                                                                                                                                        buffer[
                                                                                                                                                                                            i] & 0x02) << 6 | (
                                                                                                                                                                                                                  buffer[
                                                                                                                                                                                                                      i] & 0x01) << 1

    def generate_upnet(self, mac_address, local_ip, number, password):
        packet = []
        packet.append(1)
        packet_len = len(number) + len(password) + 60
        packet.append(packet_len)
        packet.extend([i * 0 for i in range(16)])
        packet.extend([7, 8])
        packet.extend([int(i, 16) for i in mac_address.split(':')])
        packet.extend([1, len(number) + 2])
        packet.extend([ord(i) for i in number])
        packet.extend([2, len(password) + 2])
        packet.extend([ord(i) for i in password])
        packet.extend([9, len(local_ip) + 2])
        packet.extend([ord(i) for i in local_ip])
        packet.extend([10, 5, 105, 110, 116, 14, 3, 1, 31, 7, 51, 46, 54, 46, 53])
        md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
        packet[2:18] = struct.unpack('16B', md5)
        self.encrypt(packet)
        packet = ''.join([struct.pack('B', i) for i in packet])
        return packet

    def generate_breathe(self, mac_address, local_ip, session, index):
        index = hex(index)[2:]
        packet = []
        packet.append(3)
        packet_len = len(session) + 88
        packet.append(packet_len)
        packet.extend([i * 0 for i in range(16)])
        packet.extend([8, len(session) + 2])
        packet.extend(session)
        packet.extend([9, 18])
        packet.extend([ord(i) for i in local_ip])
        packet.extend([i * 0 for i in range(16 - len(local_ip))])
        packet.extend([7, 8])
        packet.extend([int(i, 16) for i in mac_address.split(':')])
        packet.extend([20, 6])
        packet.extend([int(index[0:-6], 16), int(index[-6:-4], 16), int(index[-4:-2], 16), int(index[-2:], 16)])
        packet.extend(
            [42, 6, 0, 0, 0, 0, 43, 6, 0, 0, 0, 0, 44, 6, 0, 0, 0, 0, 45, 6, 0, 0, 0, 0, 46, 6, 0, 0, 0, 0, 47, 6, 0, 0,
             0, 0])
        md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
        packet[2:18] = struct.unpack('16B', md5)
        self.encrypt(packet)
        packet = ''.join([struct.pack('B', i) for i in packet])
        return packet

    def generate_downnet(self, mac_address, local_ip, session, index):
        index = hex(index)[2:]
        packet = []
        packet.append(5)
        packet_len = len(session) + 88
        packet.append(packet_len)
        packet.extend([i * 0 for i in range(16)])
        packet.extend([8, len(session) + 2])
        packet.extend(session)
        packet.extend([9, 18])
        packet.extend([ord(i) for i in local_ip])
        packet.extend([i * 0 for i in range(16 - len(local_ip))])
        packet.extend([7, 8])
        packet.extend([int(i, 16) for i in mac_address.split(':')])
        packet.extend([20, 6])
        packet.extend([int(index[0:-6], 16), int(index[-6:-4], 16), int(index[-4:-2], 16), int(index[-2:], 16)])
        packet.extend(
            [42, 6, 0, 0, 0, 0, 43, 6, 0, 0, 0, 0, 44, 6, 0, 0, 0, 0, 45, 6, 0, 0, 0, 0, 46, 6, 0, 0, 0, 0, 47, 6, 0, 0,
             0, 0])
        md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
        packet[2:18] = struct.unpack('16B', md5)
        self.encrypt(packet)
        packet = ''.join([struct.pack('B', i) for i in packet])
        return packet


if __name__ == "__main__":
    app = FuckTheSupplicant()
    app.run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import json
import socket
import struct
import sys
import threading
import time
import uuid
import wx
import main_frame


class Link(main_frame.mainFrame):

    def __init__(self, parent):
        super(Link, self).__init__(parent)
        self.local_ip = self.get_local_ip()
        self.host = self.get_host()
        self.number = ""
        self.password = ""
        self.mac_address = ""
        self.on_line = 0
        self.on_count = 0

    # 获取本地MAC地址
    def get_mac_address(self):
        mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac_address[e:e + 2] for e in range(0, 11, 2)])

    # 获取远程服务器Host
    def get_host(self):
        host = '219.218.154.250'  # For YTU
        return host

    # 获取本地IP地址
    def get_local_ip(self):
        try:
            csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            csock.connect(('8.8.8.8', 80))
            (addr, port) = csock.getsockname()
            csock.close()
            return addr
        except socket.error:
            return "127.0.0.1"

    # 保存数据
    def save_config(self, mac_address, host, number, password):
        if not self.checkPassword.GetValue():
            number = ''
            password = ''

        config = {
            'host': host,
            'mac_address': mac_address,
            'number': number,
            'password': password,
            'version': '0.1.1',
            'bug_report': 'i@mayuko.cn'
        }
        js_config = json.dumps(config)
        file_object = open('config.fts', 'w')
        file_object.write(js_config)
        file_object.close()

    # 初始化数据
    def init_data(self):
        try:
            js_config = ''
            for line in open("config.fts"):
                js_config = line
            config = json.loads(js_config)
            self.macInput.SetValue(config['mac_address'])
            self.hostInput.SetValue(config['host'])
            self.numberInput.SetValue(config['number'])
            if config['password'] != '':
                self.passwordInput.SetValue(config['password'])
        except IOError:
            mac_address = self.get_mac_address()
            host = self.get_host()
            self.macInput.SetValue(mac_address)
            self.hostInput.SetValue(host)
            self.save_config(host, mac_address, "", "")

    # 初始化主窗口
    def init_main_window(self):
        self.init_data()
        self.statusBar.SetStatusText(u"等待连接", 0)
        self.statusBar.SetStatusText(u"本地IP：" + self.local_ip, 1)

    # 输入密码
    def on_text_changed(self, event):
        self.loginButton.Enable()

    # 尝试连接
    def link_button_click(self, event):
        if int(self.statusFlag.GetValue()) == 0:
            self.statusBar.SetStatusText(u"正在连接", 0)
            self.loginButton.Disable()
            self.mac_address = self.macInput.GetValue()
            self.local_ip = self.get_local_ip()
            self.print_console(u"本地IP：" + self.local_ip)
            self.host = self.hostInput.GetValue()
            self.number = self.numberInput.GetValue()
            self.password = self.passwordInput.GetValue()
            self.t_link = threading.Thread(target=self.creat_process,
                                           args=(
                                               self.mac_address, self.local_ip, self.host, self.number, self.password,))
            self.t_link.start()
        else:
            self.disconnect()

    # 创建子进程
    def creat_process(self, mac_address, local_ip, host, number, password):
        self.connect(mac_address, local_ip, host, number, password)

    # 上线
    def connect(self, mac_address, local_ip, host, number, password):
        print u"try connect"
        self.print_console(u"正在连接")
        self.link_attempts = 0
        self.save_config(mac_address, host, number, password)
        self.index = 0x01000000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)
        while self.link_attempts < 8 and int(self.statusFlag.GetValue()) != 1:
            # print "statusFlag is " + self.statusFlag.GetValue()
            try:
                upnet_packet = self.generate_upnet(mac_address, local_ip, number, password)
                session = self.upnet(self.sock, upnet_packet)
                self.breathe(self.sock, mac_address, local_ip, session, self.index)
            except Exception, e:
                # print u"link_attempts is " + str(self.link_attempts)
                self.link_attempts = self.link_attempts + 1
                self.statusBar.SetStatusText(u"尝试重新连接", 0)
                self.print_console(u"尝试重新连接")
                if self.verboseMode.GetValue():
                    self.print_console(str(e))

        self.loginButton.Enable()
        self.statusBar.SetStatusText(u"连接超时", 0)
        self.print_console(u"连接超时")

    # 下线
    def disconnect(self):
        self.init_link()
        downnet_packet = self.generate_downnet(self.mac_address, self.local_ip, self.session, self.index)
        self.send(self.sock, downnet_packet)
        self.sock.close()
        self.t_link.join(0)  # 删除子线程
        self.print_console(u"下线成功")
        self.dialog(u"下线成功")

    # 初始化连接
    def init_link(self):
        self.statusFlag.SetValue("0")
        self.statusBar.SetStatusText(u"等待连接", 0)
        self.loginButton.SetLabel(u"连接")
        self.macInput.Enable()
        self.hostInput.Enable()
        self.numberInput.Enable()
        self.passwordInput.Enable()
        self.checkPassword.Enable()

    # 显示通知
    def dialog(self, msg):
        self.msgDialog.SetMessage(msg)
        self.msgDialog.ShowModal()

    # 打印消息
    def print_console(self, msg):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.consoleText.SetValue(self.consoleText.GetValue() + ">" + now_time + " " + msg + "\n")
        line = self.consoleText.GetNumberOfLines() - 1
        self.consoleText.ShowPosition(
            self.consoleText.XYToPosition(self.consoleText.GetLineLength(line - 7), line - 7))  # 显示最后一行信息

    # 启动Timer
    def take_timer(self):
        self.timer.Start(1000)
        print u"start timer"

    def on_timer(self, event):
        self.on_count = self.on_count + 1
        print u"count is " + str(self.on_count)

    # 发送sock
    def send(self, sock, packet):
        host = self.host
        port = 3848
        sock.sendto(packet, (host, port))

    # sock连接
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
        self.loginButton.Enable()
        if 0 == int(upnet_ret[20]):
            self.print_console(u"连接失败\n" + message)
            self.statusBar.SetStatusText(u"密码或MAC错误", 0)
            self.dialog(message)
        else:
            self.statusBar.SetStatusText(u"已连接", 0)
            self.statusFlag.SetValue("1")
            self.macInput.Disable()
            self.hostInput.Disable()
            self.numberInput.Disable()
            self.passwordInput.Disable()
            self.checkPassword.Disable()
            self.loginButton.SetLabel(u"下线")
            self.print_console(u"连接成功\n" + message)
            return session

    # 保持连接
    def breathe(self, sock, mac_address, local_ip, session, index):
        time.sleep(0)
        while True and int(self.statusFlag.GetValue()) == 1:
            # print(u"keep online")
            if self.verboseMode.GetValue():
                self.print_console(u"keep breathe")
            breathe_packet = self.generate_breathe(mac_address, local_ip, session, index)
            self.send(sock, breathe_packet)
            try:
                breathe_ret = sock.recv(3848)
            except socket.timeout:
                if self.verboseMode.GetValue():
                    self.print_console(u"socket timeout, continue")
                continue
            else:
                status = struct.unpack('B' * len(breathe_ret), breathe_ret)
                if self.verboseMode.GetValue():
                    self.print_console(u"socket status is " + str(status[20]))
                if status[20] == 0:
                    self.init_link()
                    self.print_console(u"网络连接失败")
                    # 如果开启掉线重连选项
                    if self.reLink:
                        self.t_link.join(0)
                        self.print_console(u"尝试自动重连")
                        self.t_link = threading.Thread(target=self.creat_process,
                                                       args=(self.mac_address, self.local_ip, self.host, self.number,
                                                             self.password,))
                        self.t_link.start()
                    else:
                        self.dialog(u"网络已断开，请检查网络连接")
                index += 3

    # 加密
    def encrypt(self, buffer):
        for i in range(len(buffer)):
            buffer[i] = (buffer[i] & 0x80) >> 6 | (buffer[i] & 0x40) >> 4 | (buffer[i] & 0x20) >> 2 | (
                    buffer[i] & 0x10) << 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 2 | (
                                buffer[i] & 0x02) >> 1 | (buffer[i] & 0x01) << 7

    # 解密
    def decrypt(self, buffer):
        for i in range(len(buffer)):
            buffer[i] = (buffer[i] & 0x80) >> 7 | (buffer[i] & 0x40) >> 2 | (buffer[i] & 0x20) >> 2 | (
                    buffer[i] & 0x10) >> 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 4 | (
                                buffer[i] & 0x02) << 6 | (buffer[i] & 0x01) << 1

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

    def on_close(self, event):
        if int(self.statusFlag.GetValue()) == 1:
            msgbox = wx.MessageDialog(
                None, u"关闭后将无法保持连接", u'确定关闭吗？', wx.YES_NO | wx.ICON_QUESTION)
            result = msgbox.ShowModal()
            if (result == wx.ID_YES):
                self.disconnect()
                sys.exit()
        else:
            sys.exit()


if __name__ == '__main__':
    app = wx.App()
    main_win = Link(None)
    main_win.init_main_window()
    main_win.Show()
    app.MainLoop()

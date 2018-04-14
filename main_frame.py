# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx._xml

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Fuck The Supplicant", pos=wx.DefaultPosition,
                          size=wx.Size(300, 430),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(300, 430), wx.Size(300, 430))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        icon = wx.Icon()
        icon.LoadFile(u"app.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        # self.tbicon = wx.adv.TaskBarIcon()
        # self.tbicon.SetIcon(icon, "wxPython Demo")
        self.msgDialog = wx.MessageDialog(None, u"", u"通知", wx.OK | wx.ICON_INFORMATION)

        mainLayout = wx.WrapSizer(wx.VERTICAL)

        self.consoleText = wx.TextCtrl(self, wx.ID_ANY, u">Fuck The Supplicant\n", wx.DefaultPosition,
                                       wx.Size(300, 120), wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        self.consoleText.SetFont(
            wx.Font(8, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        self.consoleText.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        mainLayout.Add(self.consoleText, 0, wx.ALL, 5)

        self.settingPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.DOUBLE_BORDER | wx.TAB_TRAVERSAL)
        self.settingPanel.SetMinSize(wx.Size(300, -1))

        settingLayout = wx.BoxSizer(wx.VERTICAL)

        hostLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.hostLable = wx.StaticText(self.settingPanel, wx.ID_ANY, u"远程服务器", wx.DefaultPosition, wx.DefaultSize, 0)
        self.hostLable.Wrap(-1)
        hostLayout.Add(self.hostLable, 0, wx.ALL, 5)

        self.hostInput = wx.TextCtrl(self.settingPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     0)
        self.hostInput.SetMinSize(wx.Size(200, -1))

        hostLayout.Add(self.hostInput, 0, wx.ALL, 5)

        settingLayout.Add(hostLayout, 1, wx.EXPAND, 5)

        macLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.macLable = wx.StaticText(self.settingPanel, wx.ID_ANY, u"MAC地址  ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.macLable.Wrap(-1)
        macLayout.Add(self.macLable, 0, wx.ALL, 5)

        self.statusFlag = wx.TextCtrl(self.settingPanel, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.statusFlag.Hide()

        macLayout.Add(self.statusFlag, 0, wx.ALL, 5)

        self.macInput = wx.TextCtrl(self.settingPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.macInput.SetMinSize(wx.Size(200, -1))

        macLayout.Add(self.macInput, 0, wx.ALL, 5)

        settingLayout.Add(macLayout, 1, wx.EXPAND, 5)

        self.settingPanel.SetSizer(settingLayout)
        self.settingPanel.Layout()
        settingLayout.Fit(self.settingPanel)
        mainLayout.Add(self.settingPanel, 1, wx.EXPAND | wx.ALL, 5)

        self.loginPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.DOUBLE_BORDER | wx.TAB_TRAVERSAL)
        loginLayout = wx.BoxSizer(wx.VERTICAL)

        numberLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.numberLable = wx.StaticText(self.loginPanel, wx.ID_ANY, u"账号名称   ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.numberLable.Wrap(-1)
        numberLayout.Add(self.numberLable, 0, wx.ALL, 5)

        self.numberInput = wx.TextCtrl(self.loginPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       0)
        self.numberInput.SetMinSize(wx.Size(200, -1))

        numberLayout.Add(self.numberInput, 0, wx.ALL, 5)

        loginLayout.Add(numberLayout, 1, wx.EXPAND, 5)

        passwordLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.passwordLable = wx.StaticText(self.loginPanel, wx.ID_ANY, u"账号密码   ", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.passwordLable.Wrap(-1)
        passwordLayout.Add(self.passwordLable, 0, wx.ALL, 5)

        self.passwordInput = wx.TextCtrl(self.loginPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         wx.TE_PASSWORD)
        self.passwordInput.SetMinSize(wx.Size(200, -1))

        passwordLayout.Add(self.passwordInput, 0, wx.ALL, 5)

        loginLayout.Add(passwordLayout, 1, wx.EXPAND, 5)

        checkLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.checkPassword = wx.CheckBox(self.loginPanel, wx.ID_ANY, u"记住密码", wx.DefaultPosition, wx.DefaultSize, 0)
        self.checkPassword.SetValue(True)
        checkLayout.Add(self.checkPassword, 0, wx.ALL, 5)

        self.reLink = wx.CheckBox(self.loginPanel, wx.ID_ANY, u"掉线重连", wx.DefaultPosition, wx.DefaultSize, 0)
        self.reLink.SetValue(True)
        checkLayout.Add(self.reLink, 0, wx.ALL, 5)

        self.verboseMode = wx.CheckBox(self.loginPanel, wx.ID_ANY, u"VerboseMode", wx.DefaultPosition, wx.DefaultSize,
                                       0)
        checkLayout.Add(self.verboseMode, 0, wx.ALL, 5)

        loginLayout.Add(checkLayout, 1, wx.EXPAND, 5)

        self.loginPanel.SetSizer(loginLayout)
        self.loginPanel.Layout()
        loginLayout.Fit(self.loginPanel)
        mainLayout.Add(self.loginPanel, 1, wx.EXPAND | wx.ALL, 5)

        self.loginButton = wx.Button(self, wx.ID_ANY, u"连接", wx.DefaultPosition, wx.DefaultSize, 0)
        self.loginButton.Enable(False)
        self.loginButton.SetMinSize(wx.Size(300, -1))

        mainLayout.Add(self.loginButton, 0, wx.ALL, 5)

        self.SetSizer(mainLayout)
        self.Layout()
        self.statusBar = self.CreateStatusBar(2, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.timer = wx.Timer()
        self.timer.SetOwner(self, wx.ID_ANY)

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.passwordInput.Bind(wx.EVT_TEXT, self.on_text_changed)
        self.loginButton.Bind(wx.EVT_BUTTON, self.link_button_click)
        self.Bind(wx.EVT_TIMER, self.on_timer, id=wx.ID_ANY)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def on_close(self, event):
        event.Skip()

    def on_text_changed(self, event):
        event.Skip()

    def link_button_click(self, event):
        event.Skip()

    def on_timer(self, event):
        event.Skip()



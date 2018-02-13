#!/bin/python
"""
Hello World, pXTerm version 1.0
FangWenjian, fwjse1992@gmail.com
"""

import wx
import sys
import logging

from pXTermCONFIG import pXTermCONFIG
from pXTermSSH import pXTermSSH

logger = logging.getLogger('pXTermGUI')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

class pXTermFrame(wx.Frame):
    """
    Major Frame of pXTerm
    """
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(pXTermFrame, self).__init__(*args, **kw)

        self.sessionMenu = wx.Menu()
        self.newSessionItem = self.sessionMenu.Append(wx.ID_ANY, "&New Session")
        self.exitItem = self.sessionMenu.Append(wx.ID_EXIT)

        self.helpMenu = wx.Menu()
        self.aboutItem = self.helpMenu.Append(wx.ID_ABOUT)

        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.sessionMenu, "&Session")
        self.menuBar.Append(self.helpMenu, "&Help")

        self.SetMenuBar(self.menuBar)

        self.Bind(wx.EVT_MENU, self.OnNewSession, self.newSessionItem)
        self.Bind(wx.EVT_MENU, self.OnExit, self.exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.aboutItem)

        self.CreateStatusBar()
        self.SetStatusText("Welcome to pXTerm version 1.0")

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sessionName = ""
        self.existSessionPanel = ExistSessionPanel(self)
        grid.Add(self.existSessionPanel, pos=(0,0))
        self.nb = wx.Notebook(self)
        grid.Add(self.nb, pos=(1,0))


        hSizer.Add(grid, 0, wx.ALL, 5)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnNewSession(self, event):
        """create new session and then connect to this session."""
        #wx.MessageBox("This is new session")
        newSessionFrame = wx.Frame(self, title="Create New Session")
        NewSessionPanel(newSessionFrame)

        newSessionFrame.Show(True)
        #new window to create a new session

        # then connec to this session

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a light weight python X Terminal version 1.0.\n"
                      "Author: FangWenjian/2018.01.22 ",
                      "About pXTerm",
                      wx.OK|wx.ICON_INFORMATION)

    def OnConnect(self, sessionName):
        session = configs.get_config_by_session_name(self.sessionName)

        connectedSession = ConnectedSessionPanel(pxterm.nb)
        pxterm.nb.AddPage(connectedSession, self.sessionName)
        logger.info(session)

        sshs.connect_session(connectedSession, session[1], session[3], session[4], int(session[2]))

class NewSessionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.quote = wx.StaticText(self, label="Create New Session: ")
        grid.Add(self.quote, pos=(0,0))

        # A button
        self.button = wx.Button(self, label="Save")
        self.Bind(wx.EVT_BUTTON, self.clickSaveButton, self.button)
        self.Bind(wx.EVT_COMMAND_ENTER, self.clickSaveButton, self.button)

        # the edit control - session name.
        self.sessionNameText = wx.StaticText(self, label="Session name :")
        grid.Add(self.sessionNameText, pos=(1,0))
        self.editSessionName = wx.TextCtrl(self, size=(140,-1))
        grid.Add(self.editSessionName, pos=(1,1))

        # the edit control - session ip.
        self.sessionIPText = wx.StaticText(self, label="IP addr :")
        grid.Add(self.sessionIPText, pos=(2,0))
        self.editSessionIP = wx.TextCtrl(self, size=(140,-1))
        grid.Add(self.editSessionIP, pos=(2,1))

        # the combobox Control
        self.portList = ['22']
        self.portText = wx.StaticText(self, label="port")
        grid.Add(self.portText, pos=(3,0))
        self.portBox = wx.ComboBox(self, value='22', size=(95, -1), choices=self.portList, style=wx.CB_DROPDOWN)
        grid.Add(self.portBox, pos=(3,1))

        # the edit control - login account.
        self.loginText = wx.StaticText(self, label="Login account :")
        grid.Add(self.loginText, pos=(4,0))
        self.loginAccount = wx.TextCtrl(self, size=(140,-1))
        grid.Add(self.loginAccount, pos=(4,1))


        # the edit control - login password.
        self.passwordText = wx.StaticText(self, label="Login password :")
        grid.Add(self.passwordText, pos=(5,0))
        self.password = wx.TextCtrl(self, size=(140,-1), style = wx.TE_PASSWORD)
        grid.Add(self.password, pos=(5,1))


        hSizer.Add(grid, 0, wx.ALL, 5)

        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.button, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

    def clickSaveButton(self, event):
        sn = self.editSessionName.GetValue()
        sip = self.editSessionIP.GetValue()
        sport = self.portBox.GetValue()
        slogin = self.loginAccount.GetValue()
        spass = self.password.GetValue()
        logger.info("session name: " + sn)
        logger.info("session ip: " + sip)
        logger.info("session port: " + sport)
        logger.info("session login account: " + slogin)
        logger.info("session login password: " + spass)
        session = [sn, sip, sport, slogin, spass]
        if(configs.write_config(session) == True):
            wx.MessageBox("Save the new session", "New Session", wx.OK|wx.ICON_INFORMATION)
            self.parent.Close(True)
        else:
            wx.MessageBox("The session name Exist, please check", "New Session",
                          wx.OK | wx.ICON_INFORMATION)

class ExistSessionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.quote = wx.StaticText(self, label="Exist Sessions: ")
        grid.Add(self.quote, pos=(0,0))

        self.sessionsName = configs.get_all_sessions_name()
        # the edit control - session name.
        sessionList = []
        for name in self.sessionsName:
            session = configs.get_config_by_session_name(name)
            sessionList.append((session[0] + '[' + session[1]) + ']')

        self.sessionListBox = wx.ListBox(self, wx.ID_ANY, size=self.GetMaxSize(), choices=sessionList, style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.ConnectSession, self.sessionListBox)

        grid.Add(self.sessionListBox, pos=(1,0))

        hSizer.Add(grid, 0, wx.ALL, 5)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)

    def ConnectSession(self, event):
        logger.info("session: " + event.GetEventObject().GetStringSelection())
        sessionName = (event.GetEventObject().GetStringSelection()).split('[')[0]
        logger.info("session name: "+sessionName)
        pxterm.sessionName = sessionName

        logger.info("pxterm session name: " + pxterm.sessionName)
        pxterm.OnConnect(pxterm.sessionName)

class ConnectedSessionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #sshs.connect_session(session[1], session[3], session[4], int(session[2]))


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    configs = pXTermCONFIG('sessions')
    sshs = pXTermSSH()
    pxterm = pXTermFrame(None, title='pXTerm version 1.0')

    pxterm.Show()
    app.MainLoop()

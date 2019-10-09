import wx

class SimpleGuiMenu():
    def __init__(self, parent):
        self.parent = parent
        self._addMenubar()

    def _addMenubar(self):
        self.menubar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        self.menubar.Append(self.fileMenu, '&File')

        helpMenu = wx.Menu()
        aboutItemId = wx.NewId()
        aboutItem = helpMenu.Append(aboutItemId, 'About', 'About')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnAbout, aboutItem)
        self.menubar.Append(helpMenu, '&Help')

        self.parent.SetMenuBar(self.menubar)

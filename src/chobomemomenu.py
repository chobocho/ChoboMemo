import wx
from simpleguimenu import *

class ChoboMemoMenu(SimpleGuiMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.OnAddMenu()

    def OnAddMenu(self):
        saveItemId = wx.NewId()
        saveItem = self.fileMenu.Append(saveItemId, 'Save as Text', 'Save as Text without tag')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSaveAsTextWithoutTag, saveItem)

        showSearchMenuItemId = wx.NewId()
        showSearchMenuItem = self.fileMenu.Append(showSearchMenuItemId, 'Show search menu', 'Show search menu')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnShowSearchMenu, showSearchMenuItem)

        hideSearchMenuItemId = wx.NewId()
        hideSearchMenuItem = self.fileMenu.Append(hideSearchMenuItemId, 'Hide search menu', 'Hide search menu')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnHideSearchMenu, hideSearchMenuItem)

        fileItem = self.fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit App')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnQuit, fileItem)
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

        fileItem = self.fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit App')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnQuit, fileItem)
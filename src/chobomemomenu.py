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

        self.one_tile_item_id = wx.NewId()
        one_tile_item = self.viewMenu.Append(self.one_tile_item_id, '&One', 'Show one text')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_show_1_tile, one_tile_item)

        self.two_tile_item_id = wx.NewId()
        two_tile_item = self.viewMenu.Append(self.two_tile_item_id, '&Two', 'Show two text')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_show_2_tile, two_tile_item)

        self.four_tile_item_id = wx.NewId()
        four_tile_item = self.viewMenu.Append(self.four_tile_item_id, '&Four', 'Show four text')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_show_4_tile, four_tile_item)

        self.nine_tile_item_id = wx.NewId()
        nine_tile_item = self.viewMenu.Append(self.nine_tile_item_id, '&Nine', 'Show nine text')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_show_9_tile, nine_tile_item)

        self.sixteen_tile_item_id = wx.NewId()
        sixteen_tile_item = self.viewMenu.Append(self.sixteen_tile_item_id, '&Sixteen', 'Show All text')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_show_16_tile, sixteen_tile_item)
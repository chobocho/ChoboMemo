import wx
import ChoboMemoPanel
import CommandInterpreter
import sys
from filedrop import *
from chobomemomenu import *
from info import *

'''
Start  : 2018.06.12
Update : 2019.10.25
'''

class ChoboMemoFrame(wx.Frame):
    def __init__(self, filename_, *args, **kw):
        super(ChoboMemoFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onCloseApp)

        ctrl_S_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onSave, id=ctrl_S_Id)
        ctrl_P_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onRunPaint, id=ctrl_P_Id)
        ctrl_R_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onRun, id=ctrl_R_Id)
        ctrl_Q_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ctrl_Q_Id)

        self.menu = ChoboMemoMenu(self)

        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('1'), self.menu.one_tile_item_id),
                                         (wx.ACCEL_CTRL, ord('2'), self.menu.two_tile_item_id),
                                         (wx.ACCEL_CTRL, ord('4'), self.menu.four_tile_item_id),
                                         (wx.ACCEL_CTRL, ord('9'), self.menu.nine_tile_item_id),
                                         (wx.ACCEL_CTRL, ord('0'), self.menu.sixteen_tile_item_id),
                                         (wx.ACCEL_CTRL, ord('S'), ctrl_S_Id),
                                         (wx.ACCEL_CTRL,  ord('S'), ctrl_S_Id ),
                                         (wx.ACCEL_CTRL,  ord('P'), ctrl_P_Id ),
                                         (wx.ACCEL_CTRL,  ord('R'), ctrl_R_Id ),
                                         (wx.ACCEL_CTRL,  ord('Q'), ctrl_Q_Id )])
        self.SetAcceleratorTable(accel_tbl)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.memoPanel = ChoboMemoPanel.ChoboMemoPanel(self)
        sizer.Add(self.memoPanel, 1, wx.EXPAND)
        self.SetSizer(sizer)

        if len(filename_) > 0:
            self.memoPanel.onLoadMemoFromFile(filename_)

        filedrop = FileDrop(self)
        self.SetDropTarget(filedrop)

    def OnCallback(self, filelist):
        loadFile = filelist[0]
        if self._isCMFile(loadFile):
            self.memoPanel.onLoadMemoFromFile(loadFile)

    def _isCMFile(self, filename_):
        if len(filename_) <= 0:
            return False
        if '.cm' in filename_.lower():
            return True
        return False           
        
    def onSave(self, event):
        print ("onSave")
        self.memoPanel.onSaveData()

    def OnSaveAsTextWithoutTag(self, event):
        print ("OnSaveWithoutTag")
        self.memoPanel.OnSaveAsTextWithoutTag()

    def onRunPaint(self, event):
        print ("onRunPaint")
        ci = CommandInterpreter.CommandInterpreter()
        ci.run("mspaint")

    def onRun(self, event):
        print("onRun")
        dlg = wx.TextEntryDialog(None, 'Input command','Run')
        dlg.SetValue("")

        command = "-1"
        if dlg.ShowModal() == wx.ID_OK:
            command = dlg.GetValue()
        dlg.Destroy()
        print (command)
        if command != "-1":
            ci = CommandInterpreter.CommandInterpreter()
            ci.run(command)

    def OnShowSearchMenu(self, event):
        print("OnShowSearchMenu")
        self.memoPanel.OnToggleSearchBox(True)

    def OnHideSearchMenu(self, event):    
        print("OnHideSearchMenu")
        self.memoPanel.OnToggleSearchBox(False)

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        msg = SW_TITLE \
              + '\n\nCtrl+1\nCtrl+2\nCtrl+4\nCtrl+9\nCtrl+0\n\n' \
              + '\nhttp://chobocho.com'
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

    def onCloseApp(self, event):
        if event.CanVeto() and self.memoPanel.needSave():
            try:
               dlg = wx.MessageDialog(self, 'Do you want to save before quit?',
                        'ChoboMemo', wx.YES_NO | wx.ICON_QUESTION)
               if dlg.ShowModal() == wx.ID_YES:
                   self.memoPanel.onSaveData()
               dlg.Destroy()
            except:
               dlg = wx.MessageDialog(self, 'Exception happened during closing ChoboMemo!',
                        'ChoboMemo', wx.OK | wx.ICON_INFORMATION)
               dlg.ShowModal()
               dlg.Destroy()
        self.Destroy()

    def on_show_1_tile(self, event):
        self.memoPanel.on_update_tile(1)

    def on_show_2_tile(self, event):
        self.memoPanel.on_update_tile(2)

    def on_show_4_tile(self, event):
        self.memoPanel.on_update_tile(4)

    def on_show_9_tile(self, event):
        self.memoPanel.on_update_tile(9)

    def on_show_16_tile(self, event):
        self.memoPanel.on_update_tile(16)


def main(fileName = ""):
    app = wx.App()
    frm = ChoboMemoFrame(fileName, None, title=SW_TITLE, size=(700, 640))
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1][-3:].lower() == '.cm':
        print(sys.argv[1])
        main(sys.argv[1])
    else :
        main()
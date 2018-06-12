import wx
import ChoboMemoPanel
import CommandInterpreter


'''
Start  : 2018.06.12
Update : 2018.06.13
'''

SW_TITLE = "ChoboMemo V0627.0613a"

class ChoboMemoFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(ChoboMemoFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onCloseApp)

        ctrl_S_Id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onSave, id=ctrl_S_Id)
        ctrl_P_Id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onRunPaint, id=ctrl_P_Id)
        ctrl_R_Id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onRun, id=ctrl_R_Id)
        ctrl_Q_Id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onClose, id=ctrl_Q_Id)


        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('S'), ctrl_S_Id ),
                                         (wx.ACCEL_CTRL,  ord('P'), ctrl_P_Id ),
                                         (wx.ACCEL_CTRL,  ord('R'), ctrl_R_Id ),
                                         (wx.ACCEL_CTRL,  ord('Q'), ctrl_Q_Id )])
        self.SetAcceleratorTable(accel_tbl)

        self.memoPanel = ChoboMemoPanel.ChoboMemoPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.memoPanel, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def onSave(self, event):
        print ("onSave")
        self.memoPanel.onSaveData()

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

    def onClose(self, event):
        self.Close()

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


def main(): 
    app = wx.App()
    frm = ChoboMemoFrame(None, title=SW_TITLE, size=(700, 770))
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
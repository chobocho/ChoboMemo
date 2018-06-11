import wx
import os
import FileManager

class ChoboMemoPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ChoboMemoPanel, self).__init__(*args, **kw)
        self.frame = args[0]
        self.fileManger = FileManager.FileManager()
        self.memoCtrlList = []
        self.drawUI()

    def onLoadMemo(self, evt):
        print ("onLoadMemo")
        path = ""
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="*.cm",
            style=wx.FD_OPEN | 
                  #wx.FD_MULTIPLE |
                  wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                  wx.FD_PREVIEW
            )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if len(path) > 0:
            memoData = self.fileManger.onLoad(path)
            print(memoData)
            i = 0
            for memo in self.memoCtrlList:
                memo.SetValue(memoData[i])
                i += 1
            self.frame.SetTitle("# " + path)

    def onSaveData(self):
        print ("onSaveData")
        memoData = []
        for memo in self.memoCtrlList:
            memoData.append(memo.GetValue())
        self.fileManger.onSaveData(memoData)

    def onSave(self, evt):
        print ("onSave")
        self.onSaveData()

    def onSaveMemo(self, evt):
        print ("onSaveMemo")
        saveFilePath = ""
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard="*.cm", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )
        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            saveFilePath = dlg.GetPath()
        dlg.Destroy()

        if len(saveFilePath) > 0:
            memoData = []
            for memo in self.memoCtrlList:
                tmpData = memo.GetValue()
                if len(tmpData) == 0:
                    tmpData = ""
                memoData.append(tmpData)
            self.fileManger.onSave(saveFilePath, memoData)
            self.frame.SetTitle("# " + saveFilePath)

    def onClearAll(self, evt):
        print("onClearAll")
        for memo in self.memoCtrlList:
            memo.SetValue("")

    def onExportMemo(self, evt):
        print ("onExportMemo")
        htmlFilePath = ""
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard="Html file (*.html)|*.htm", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )
        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            htmlFilePath = dlg.GetPath()
        dlg.Destroy()

        if len(htmlFilePath) > 0:
            memoData = []
            for memo in self.memoCtrlList:
                tmpData = memo.GetValue()
                if len(tmpData) == 0:
                    tmpData = ""
                memoData.append(tmpData)
            self.fileManger.exportToHtml(htmlFilePath, memoData)

    def onRunCmd(self, evt):
        tmpCmd = self.cmdText.GetValue().strip()
        self.cmdText.SetValue("")

        if len(tmpCmd) == 0:
           self.urlManger.update()
           return
        print (tmpCmd)

        if '/' in tmpCmd[0].lower():
            if len(tmpCmd) > 1:
                self.urlManger.updateWithFilter(tmpCmd[1:])
            else:
                self.urlManger.update()
        elif UrlManager.UrlManager.isURL(tmpCmd):
            self.urlManger.openURL(tmpCmd)

    def needSave(self):
        return False



    def drawUI(self):
        print ("ChoboMemoPanel::drawUI")
        sizer = wx.BoxSizer(wx.VERTICAL)

        ##
        memoMngBox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText1 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText1.SetValue("")
        memoMngBox1.Add(self.memoText1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText2 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText2.SetValue("")
        memoMngBox1.Add(self.memoText2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText3 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText3.SetValue("")
        memoMngBox1.Add(self.memoText3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText4 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText4.SetValue("")
        memoMngBox1.Add(self.memoText4, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(memoMngBox1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
 
        ##
        memoMngBox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText5 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText5.SetValue("")
        memoMngBox2.Add(self.memoText5, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText6 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText6.SetValue("")
        memoMngBox2.Add(self.memoText6, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText7 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText7.SetValue("")
        memoMngBox2.Add(self.memoText7, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText8 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText8.SetValue("")
        memoMngBox2.Add(self.memoText8, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(memoMngBox2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
 
        ##
        memoMngBox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText9 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText9.SetValue("")
        memoMngBox3.Add(self.memoText9, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText10 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText10.SetValue("")
        memoMngBox3.Add(self.memoText10, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText11 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText11.SetValue("")
        memoMngBox3.Add(self.memoText11, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText12 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText12.SetValue("")
        memoMngBox3.Add(self.memoText12, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(memoMngBox3, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
 
        ##
        memoMngBox4 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText13 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText13.SetValue("")
        memoMngBox4.Add(self.memoText13, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText14 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText14.SetValue("")
        memoMngBox4.Add(self.memoText14, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText15 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText15.SetValue("")
        memoMngBox4.Add(self.memoText15, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoText16 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(180,180))
        self.memoText16.SetValue("")
        memoMngBox4.Add(self.memoText16, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(memoMngBox4, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        ##
        memoMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        self.LoadBtn = wx.Button(self, 10, "Load", size=(30,30))
        self.LoadBtn.Bind(wx.EVT_BUTTON, self.onLoadMemo)
        memoMngBtnBox.Add(self.LoadBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.SaveBtn = wx.Button(self, 10, "Save", size=(30,30))
        self.SaveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        memoMngBtnBox.Add(self.SaveBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.SaveAsBtn = wx.Button(self, 10, "SaveAs", size=(30,30))
        self.SaveAsBtn.Bind(wx.EVT_BUTTON, self.onSaveMemo)
        memoMngBtnBox.Add(self.SaveAsBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.ExportBtn = wx.Button(self, 10, "Export", size=(30,30))
        self.ExportBtn.Bind(wx.EVT_BUTTON, self.onExportMemo)
        memoMngBtnBox.Add(self.ExportBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.memoClearAllBtn = wx.Button(self, 10, "ClearAll", size=(30,30))
        self.memoClearAllBtn.Bind(wx.EVT_BUTTON, self.onClearAll)
        memoMngBtnBox.Add(self.memoClearAllBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(memoMngBtnBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        ##
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.memoCtrlList.append(self.memoText1)
        self.memoCtrlList.append(self.memoText2)
        self.memoCtrlList.append(self.memoText3)
        self.memoCtrlList.append(self.memoText4)
        self.memoCtrlList.append(self.memoText5)
        self.memoCtrlList.append(self.memoText6)
        self.memoCtrlList.append(self.memoText7)
        self.memoCtrlList.append(self.memoText8)
        self.memoCtrlList.append(self.memoText9)
        self.memoCtrlList.append(self.memoText10)
        self.memoCtrlList.append(self.memoText11)
        self.memoCtrlList.append(self.memoText12)
        self.memoCtrlList.append(self.memoText13)
        self.memoCtrlList.append(self.memoText14)
        self.memoCtrlList.append(self.memoText15)
        self.memoCtrlList.append(self.memoText16)
import wx
import os
import FileManager
import choboutil

class ChoboMemoPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ChoboMemoPanel, self).__init__(*args, **kw)
        self.frame = args[0]
        self.hash = "0000000000000000"
        self.fileManger = FileManager.FileManager()
        self.memoCtrlList = []
        self.drawUI()

    def onLoadMemoFromFile(self, fileName):
        print ("onLoadMemoWithFile")
        memoData = self.fileManger.onLoad(fileName)
        print(memoData)
        i = 0
        for memo in self.memoCtrlList:
            memo.SetValue(memoData[i])
            i += 1
        self.frame.SetTitle("# " + fileName)
        self.hash = self.getMemoHash()

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
            self.onLoadMemoFromFile(path)

    def onSaveData(self):
        print ("onSaveData")
        memoData = []
        for memo in self.memoCtrlList:
            memoData.append(memo.GetValue())
        if self.fileManger.onSaveData(memoData) == False:
            self.onSaveNewMemo()
        self.hash = self.getMemoHash()

    def onSave(self, evt):
        print ("onSave")
        self.onSaveData()

    def onSaveNewMemo(self):
        print ("onSaveNewMemo")
        saveFilePath = ""
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard="*.cm", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

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


    def onSaveMemo(self, evt):
        print ("onSaveMemo")
        self.onSaveNewMemo()

    def onClearAll(self, evt):
        print("onClearAll")
        for memo in self.memoCtrlList:
            memo.SetValue("")

    def onExportMemo(self, evt):
        print ("onExportMemo")
        exportFilePath = ""
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard="Txt files (*.txt)|*.txt|Html file (*.htm)|*.htm", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

        if dlg.ShowModal() == wx.ID_OK:
            exportFilePath = dlg.GetPath()
        dlg.Destroy()

        if len(exportFilePath) > 0:
            print ("onExportMemo : " + exportFilePath)
            memoData = []
            for memo in self.memoCtrlList:
                tmpData = memo.GetValue()
                if len(tmpData) == 0:
                    tmpData = ""
                memoData.append(tmpData)
            if (exportFilePath[-4:].lower() == ".htm"):
                self.fileManger.exportToHtml(exportFilePath, memoData)
            else:
                self.fileManger.exportToTxt(exportFilePath, memoData)

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

    def getMemoHash(self):
        hash = ""
        for memo in self.memoCtrlList:
            tmpData = memo.GetValue()
            hash = hash + str(choboutil.hash(tmpData))
        print ("getMemoHash : " + hash)
        return hash

    def needSave(self):
        return self.hash != self.getMemoHash()

    def drawUI(self):
        print ("ChoboMemoPanel::drawUI")
        sizer = wx.BoxSizer(wx.VERTICAL)

        ##
        memoMngBox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText1 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText1.SetValue("")
        memoMngBox1.Add(self.memoText1, 1, wx.EXPAND)

        self.memoText2 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText2.SetValue("")
        memoMngBox1.Add(self.memoText2, 1, wx.EXPAND)

        self.memoText3 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText3.SetValue("")
        memoMngBox1.Add(self.memoText3, 1, wx.EXPAND)

        self.memoText4 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText4.SetValue("")
        memoMngBox1.Add(self.memoText4, 1, wx.EXPAND)

        sizer.Add(memoMngBox1, 1, wx.EXPAND)
 
        ##
        memoMngBox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText5 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText5.SetValue("")
        memoMngBox2.Add(self.memoText5, 1, wx.EXPAND)

        self.memoText6 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText6.SetValue("")
        memoMngBox2.Add(self.memoText6, 1, wx.EXPAND)

        self.memoText7 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText7.SetValue("")
        memoMngBox2.Add(self.memoText7, 1, wx.EXPAND)

        self.memoText8 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText8.SetValue("")
        memoMngBox2.Add(self.memoText8, 1, wx.EXPAND)

        sizer.Add(memoMngBox2, 1, wx.EXPAND)
 
        ##
        memoMngBox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText9 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText9.SetValue("")
        memoMngBox3.Add(self.memoText9, 1, wx.EXPAND)

        self.memoText10 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText10.SetValue("")
        memoMngBox3.Add(self.memoText10, 1, wx.EXPAND)

        self.memoText11 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText11.SetValue("")
        memoMngBox3.Add(self.memoText11, 1, wx.EXPAND)

        self.memoText12 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText12.SetValue("")
        memoMngBox3.Add(self.memoText12, 1, wx.EXPAND)

        sizer.Add(memoMngBox3, 1, wx.EXPAND)
 
        ##
        memoMngBox4 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText13 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText13.SetValue("")
        memoMngBox4.Add(self.memoText13, 1, wx.EXPAND)

        self.memoText14 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText14.SetValue("")
        memoMngBox4.Add(self.memoText14, 1, wx.EXPAND)

        self.memoText15 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText15.SetValue("")
        memoMngBox4.Add(self.memoText15, 1, wx.EXPAND)

        self.memoText16 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,150))
        self.memoText16.SetValue("")
        memoMngBox4.Add(self.memoText16, 1, wx.EXPAND)

        sizer.Add(memoMngBox4, 1, wx.EXPAND)

        ##
        memoMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        self.LoadBtn = wx.Button(self, 10, "Load", size=(30,30))
        self.LoadBtn.Bind(wx.EVT_BUTTON, self.onLoadMemo)
        memoMngBtnBox.Add(self.LoadBtn, 1, wx.EXPAND)

        self.SaveBtn = wx.Button(self, 10, "Save", size=(30,30))
        self.SaveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        memoMngBtnBox.Add(self.SaveBtn, 1, wx.EXPAND)

        self.SaveAsBtn = wx.Button(self, 10, "Save As", size=(30,30))
        self.SaveAsBtn.Bind(wx.EVT_BUTTON, self.onSaveMemo)
        memoMngBtnBox.Add(self.SaveAsBtn, 1, wx.EXPAND)

        self.ExportBtn = wx.Button(self, 10, "Export", size=(30,30))
        self.ExportBtn.Bind(wx.EVT_BUTTON, self.onExportMemo)
        memoMngBtnBox.Add(self.ExportBtn, 1, wx.EXPAND)

        self.memoClearAllBtn = wx.Button(self, 10, "ClearAll", size=(30,30))
        self.memoClearAllBtn.Bind(wx.EVT_BUTTON, self.onClearAll)
        memoMngBtnBox.Add(self.memoClearAllBtn, 1, wx.EXPAND)

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
        ##
        colorTable = [ 0, 1, 0, 1, 
                       1, 0, 1, 0,
                       0, 1, 0, 1,
                       1, 0, 1, 0]
        idx = 0;
        for memo in self.memoCtrlList:
            if colorTable[idx] == 1:
                memo.SetBackgroundColour((240, 240, 240))
            idx += 1
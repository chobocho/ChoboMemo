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
        self._OnSearchKeyword()

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
            self._OnSearchKeyword()

    def onSaveData(self):
        print ("onSaveData")
        memoData = []
        for memo in self.memoCtrlList:
            memoData.append(memo.GetValue())
        if self.fileManger.onSaveData(memoData) == False:
            self.onSaveNewMemo()
        self.hash = self.getMemoHash()

    def OnSaveAsTextWithoutTag(self):
        print ("OnSaveAsTextWithoutTag")
        exportFilePath = ""
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard="Txt files (*.txt)|*.txt|Markdown files (*.md)|*.md", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
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
            self.fileManger.exportToTxtWithoutTag(exportFilePath, memoData)

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
            defaultFile="", wildcard="Html file (*.htm)|*.htm|Txt files (*.txt)|*.txt|Markdown files (*.md)|*.md", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
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
            elif (exportFilePath[-3:].lower() == ".md"):
                self.fileManger.exportToTxtWithoutTag(exportFilePath, memoData)
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

    def OnSearchKeyword(self, event):
        print("OnSearchKeyword")
        self._OnSearchKeyword()

    def _OnSearchKeyword(self):
        self._InitMemoPanel()

        searchKeyword = self.searchKeywordText.GetValue()
        if len(searchKeyword) == 0:
            return

        tmpSearchKeywordList = searchKeyword.split('|')
        searchKeyList = []
        for k in tmpSearchKeywordList:
            if len(k) == 0:
                continue
            searchKeyList.append(k.lower())

        if len(searchKeyList) == 0:
            return

        colorList = [wx.Colour(225, 245, 254), wx.Colour(255, 248, 225), wx.Colour(255, 204, 188)]

        for memo in self.memoCtrlList:
            tmpPreData = memo.GetValue()
            if len(tmpPreData) == 0:
                continue
            tmpData = tmpPreData.lower()
            idx = 1
            for k in searchKeyList:    
                if k in tmpData:
                    # print(tmpData)
                    memo.SetBackgroundColour(colorList[idx%3])
                    memo.Refresh()
                    break
                idx += 1

    def OnClearKeyword(self, event):
        print("OnClearKeyword")
        self.searchKeywordText.SetValue("")
        self._InitMemoPanel()

    def _InitMemoPanel(self):
        colorTable = [ 0, 1, 0, 1, 
                       1, 0, 1, 0,
                       0, 1, 0, 1,
                       1, 0, 1, 0]
        font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
        idx = 0
        for memo in self.memoCtrlList:
            if colorTable[idx] == 1:
                memo.SetBackgroundColour((240, 240, 240))
            else:
                memo.SetBackgroundColour((255, 255, 255))
            memo.SetFont(font)
            memo.Refresh()
            idx += 1

    def OnToggleSearchBox(self, flag):
        if flag == True:
            self.searchKeywordText.Show()
            self.searchBtn.Show()
            self.clearSearchBtn.Show()
        else:
            self.searchKeywordText.Hide()
            self.searchBtn.Hide()
            self.clearSearchBtn.Hide()
        self.Layout()

    def drawUI(self):
        print ("ChoboMemoPanel::drawUI")
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.searchBox = wx.BoxSizer(wx.HORIZONTAL)

        self.searchKeywordText = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER, size=(580,30))
        self.searchKeywordText.SetValue("")
        self.searchKeywordText.Bind(wx.EVT_TEXT_ENTER, self.OnSearchKeyword)
        self.searchBox.Add(self.searchKeywordText, 1, wx.EXPAND)

        self.searchBtn = wx.Button(self, 10, "Search", size=(30,30))
        self.searchBtn.Bind(wx.EVT_BUTTON, self.OnSearchKeyword)
        self.searchBox.Add(self.searchBtn, 1, wx.EXPAND)

        self.clearSearchBtn = wx.Button(self, 10, "Clear", size=(30,30))
        self.clearSearchBtn.Bind(wx.EVT_BUTTON, self.OnClearKeyword)
        self.searchBox.Add(self.clearSearchBtn, 1, wx.EXPAND)

        sizer.Add(self.searchBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        ##
        BOX_SIZE = 120

        memoMngBox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText1 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText1.SetValue("")
        memoMngBox1.Add(self.memoText1, 1, wx.EXPAND)

        self.memoText2 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText2.SetValue("")
        memoMngBox1.Add(self.memoText2, 1, wx.EXPAND)

        self.memoText3 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText3.SetValue("")
        memoMngBox1.Add(self.memoText3, 1, wx.EXPAND)

        self.memoText4 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText4.SetValue("")
        memoMngBox1.Add(self.memoText4, 1, wx.EXPAND)

        sizer.Add(memoMngBox1, 1, wx.EXPAND)
 
        ##
        memoMngBox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText5 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText5.SetValue("")
        memoMngBox2.Add(self.memoText5, 1, wx.EXPAND)

        self.memoText6 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText6.SetValue("")
        memoMngBox2.Add(self.memoText6, 1, wx.EXPAND)

        self.memoText7 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText7.SetValue("")
        memoMngBox2.Add(self.memoText7, 1, wx.EXPAND)

        self.memoText8 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText8.SetValue("")
        memoMngBox2.Add(self.memoText8, 1, wx.EXPAND)

        sizer.Add(memoMngBox2, 1, wx.EXPAND)
 
        ##
        memoMngBox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText9 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText9.SetValue("")
        memoMngBox3.Add(self.memoText9, 1, wx.EXPAND)

        self.memoText10 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText10.SetValue("")
        memoMngBox3.Add(self.memoText10, 1, wx.EXPAND)

        self.memoText11 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText11.SetValue("")
        memoMngBox3.Add(self.memoText11, 1, wx.EXPAND)

        self.memoText12 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText12.SetValue("")
        memoMngBox3.Add(self.memoText12, 1, wx.EXPAND)

        sizer.Add(memoMngBox3, 1, wx.EXPAND)
 
        ##
        memoMngBox4 = wx.BoxSizer(wx.HORIZONTAL)

        self.memoText13 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText13.SetValue("")
        memoMngBox4.Add(self.memoText13, 1, wx.EXPAND)

        self.memoText14 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText14.SetValue("")
        memoMngBox4.Add(self.memoText14, 1, wx.EXPAND)

        self.memoText15 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText15.SetValue("")
        memoMngBox4.Add(self.memoText15, 1, wx.EXPAND)

        self.memoText16 = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(150,BOX_SIZE))
        self.memoText16.SetValue("")
        memoMngBox4.Add(self.memoText16, 1, wx.EXPAND)

        sizer.Add(memoMngBox4, 1, wx.EXPAND)

        ##
        memoMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        loadBtnId = wx.NewId()
        self.LoadBtn = wx.Button(self, loadBtnId, "Load", size=(30,30))
        self.LoadBtn.Bind(wx.EVT_BUTTON, self.onLoadMemo)
        memoMngBtnBox.Add(self.LoadBtn, 1, wx.EXPAND)

        saveBtnId = wx.NewId()
        self.SaveBtn = wx.Button(self, saveBtnId, "Save", size=(30,30))
        self.SaveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        memoMngBtnBox.Add(self.SaveBtn, 1, wx.EXPAND)

        saveAsBtnId = wx.NewId()
        self.SaveAsBtn = wx.Button(self, saveAsBtnId, "Save As", size=(30,30))
        self.SaveAsBtn.Bind(wx.EVT_BUTTON, self.onSaveMemo)
        memoMngBtnBox.Add(self.SaveAsBtn, 1, wx.EXPAND)

        exportBtnId = wx.NewId()
        self.ExportBtn = wx.Button(self, exportBtnId, "Export", size=(30,30))
        self.ExportBtn.Bind(wx.EVT_BUTTON, self.onExportMemo)
        memoMngBtnBox.Add(self.ExportBtn, 1, wx.EXPAND)

        memoClearAllBtnId = wx.NewId()
        self.memoClearAllBtn = wx.Button(self, memoClearAllBtnId, "ClearAll", size=(30,30))
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

        self._InitMemoPanel()
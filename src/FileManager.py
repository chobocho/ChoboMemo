import os
import wx
import json

class FileManager:
    def __init__(self):
        self.fileName = ""
        self.memo = []

    def onLoadJson(self):
       print ("onLoadJson")
       try:
           with open(self.fileName) as f:
               jsonData = json.load(f)
           print(jsonData['version'])
           self.memo = jsonData['memo'][:]
           #print(self.memo)
       except:
           print ("onLoadJson: Fail")
           return False

       return True

    def onLoad(self, filename_):
        print("Load " + filename_)
        if (os.path.isfile(filename_)) == False:
            return []

        self.fileName = filename_

        if self.onLoadJson() == True:
            return self.memo

        # For old format
        try:
            print ("onLoad...")
            f = open(self.fileName,'r')
            tmpMemo = f.read()
            memo = tmpMemo.strip().split("o(._.)p")
            print(memo)
            f.close()
            return memo
        except:
            dlg = wx.MessageDialog(None, 'Exception happened during closing ChoboMemo!',
                     'ChoboMemo', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        
        return []

    def onSaveAsJson(self, memoData):
        print("onSaveAsJson ")
        jsonData = {}
        jsonData['version'] = "V0627.1001"
        jsonData['memo'] = []

        for memo in memoData:
            jsonData['memo'].append(memo)

        f = open(self.fileName,'w')
        f.write(json.dumps(jsonData))
        f.close()

    def onSaveData(self, memoData):
        print("onSaveData ")
        if len(self.fileName) < 3:
           print ("Wrong save file name")
           return False

        self.onSaveAsJson(memoData)
        return True

    def onSave(self, filename_, memoData):
        print("onSave " + filename_)
        self.fileName = filename_
        self.onSaveData(memoData)

    def exportToHtml(self, filePath, memoData):
        try:
            htmlHead='''
            <html>
            <head>
            <title>ChoboMemo</title>
            <style>
            td {
                text-align:left;
                vertical-align: text-top;
            
            h10 {
                color:white;
            }
            
            a:link {
                text-decoration: none;
            }
            
            a:link, a:visited {
                color: blue;
            }
            </style>
            </head>
            <body>
            <center>
            <table border="1" style="border-collapse:collapse; border:1px gray solid;">
            '''
            htmlTail='''
            </table>
            </body>
            </html>
            '''
            f = open(filePath,'w')
            f.write(htmlHead)
            idx = 1
            colorTable = [ 0, 1, 0, 1, 
                           1, 0, 1, 0,
                           0, 1, 0, 1,
                           1, 0, 1, 0]

            for memo in memoData:
                if idx % 4 == 1:
                    f.write("<tr>\n")
                bgcolor = ""
                postNoSpaceData = ("&nbsp;").join(memo.split(" "))
                postData = ("<br>").join(postNoSpaceData.split("\n"))
   
                if colorTable[idx-1] == 1:
                    bgcolor = "bgcolor=#e6f2ff"
                tmpHtml = "<td {0}>&nbsp;{1}&nbsp;</td>\n".format(bgcolor, postData)
                #print(tmpHtml)
                f.write(tmpHtml)
                if idx % 4 == 0:
                    f.write("</tr>\n")
                idx += 1
            f.write(htmlTail)
            f.close()
        except:
            dlg = wx.MessageDialog(None, 'Exception happened during export to HTML!',
                     'ChoboMemo', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()


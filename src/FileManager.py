import os
import wx
import json
import traceback

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
                h10 {
                  color: white;
                }
	            
                a:link {
                  text-decoration: none;
                }
	            
                a:link,
                a:visited {
                  color: blue;
                }
	            
                .jb_table {
                  display: table;
                  margin-left: auto;
                  margin-right: auto;
                }
	            
                .row {
                  border-radius: 10px;
                  margin: 2px auto;
                  display: table-row;
                }
	            
                .cell {
                  text-align: left;
                  border-radius: 10px;
                  margin: 2px auto;
                  display: table-cell;
                  border: 1px solid blue;
                  vertical-align: top;
                }
	            
                .circle_rectangle {
                  width: 160px;
                  border-radius: 10px;
                  margin: 2px auto;
                }
	            
                .circle_bg_lightblue_rectangle {
                  border: 1px solid lightblue;
                  background-color: lightblue;
                  border-radius: 10px;
                  margin: 2px auto;
                }
	            
                .circle_bg_yellow_rectangle {
                  width: 160px;
                  border: 1px solid rgb(241, 245, 9);
                  background-color: rgb(241, 245, 9);
                  border-radius: 10px;
                  margin: 2px auto;
                }
	            
                .circle_lightblue_rectangle {
                  width: 160px;
                  border: 1px solid lightblue;
                  border-radius: 10px;
                  margin: 2px auto;
                  color: white;
                }
	            
                .circle_orange_rectangle {
                  border: 1px solid orange;
                  border-radius: 10px;
                  margin: 2px auto;
                }
	            
                .circle_orangered_rectangle {
                  border: 1px solid orangered;
                  background-color: rgb(233, 99, 50);
                  border-radius: 10px;
                  margin: 2px auto;
                }
            </style>
            </head>
            <body>
                <div class="jb_table">
                    <div class="row">
            '''
            htmlTail='''
                    </div>
                </div>
            </body>
            </html>
            '''
            f = open(filePath,'w')
            f.write(htmlHead)
            idx = 0
            colorTable = [ 0, 1, 0, 1, 
                           1, 0, 1, 0,
                           0, 1, 0, 1,
                           1, 0, 1, 0]

            rowList = ["<span class='cell'>\n"] * 4
            for memo in memoData:

                if colorTable[idx] == 0:
                    bgcolor = "class='circle_orange_rectangle'"
                else:
                    bgcolor = "class='circle_lightblue_rectangle'"
                postNoSpaceData = ("&nbsp;").join(memo.split(" "))
                postData = ("<br>").join(postNoSpaceData.split("\n"))
   
                tmpHtml = "<div {0}>&nbsp;{1}&nbsp;</div>\n".format(bgcolor, postData)
                #print(tmpHtml)
                rowList[idx%4] += tmpHtml
                idx += 1

            for i in range(4):
                rowList[i] += "</span>\n"

            for i in range(4):
                 f.write(rowList[i])

            f.write(htmlTail)
            f.close()
        except:
            #traceback.print_exc()
            dlg = wx.MessageDialog(None, 'Exception happened during export to HTML!',
                     'ChoboMemo', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()


    def exportToTxt(self, filePath, memoData):
        try:
            f = open(filePath, 'w')
            idx = 0
            for memo in memoData:
                idx += 1
                if len(memo) == 0:
                    continue
                tmpText = 'Memo {0}\n'.format(idx)
                tmpText = tmpText + memo + "\n\n\n"
                f.write(tmpText)
            f.close()
        except:
            dlg = wx.MessageDialog(None, 'Exception happened during export to TXT!',
                                   'ChoboMemo', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

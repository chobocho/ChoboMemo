import os
import wx

class FileManager:
    def __init__(self):
        self.fileName = ""

    def onLoad(self, filename_):
        print("Load" + filename_)
        self.fileName = filename_

        try:
            if (os.path.isfile(self.fileName)):
                f = open(self.fileName,'r')
                tmpMemo = f.read()
                memo = tmpMemo.strip().split("o(._.)p")
                print(memo)
                f.close()
                return memo
            else:
                return []
        except:
            dlg = wx.MessageDialog(None, 'Exception happened during closing ChoboMemo!',
                     'ChoboMemo', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        
        return []

    def onSaveData(self, memoData):
        print("onSaveData ")
        if len(self.fileName) < 3:
           print ("Wrong save file name")
           return False

        f = open(self.fileName,'w')
        for memo in memoData:
            tmpMemo = memo + "o(._.)p"
            f.write(tmpMemo)
        f.close()
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
            <title>ChoboFileManager2 URL list</title>
            <style>
            td {
                text-align:center
            }
            
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
            for memo in memoData:
                if idx % 4 == 1:
                    f.write("<tr>\n")
                bgcolor = ""
                if idx % 2 == 0:
                    bgcolor = "bgcolor=#e6f2ff"
                tmpHtml = "<td {0}>&nbsp;{1}&nbsp;</td>\n".format(bgcolor, memo)
                print(tmpHtml)
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


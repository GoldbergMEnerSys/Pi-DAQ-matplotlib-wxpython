import wx
import sys
import subprocess



class myFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(myFrame, self).__init__(*args, **kw)
        self.InitUI()
        print "started"

    def InitUI(self):      
        
        self.SetSize((500,500))
        self.SetTitle("Frame")
        self.Show(True)

        self.label = wx.StaticText(self, label = "Hello World", pos = (100,50))
        
        self.txtDigipot = wx.TextCtrl(self, size =(100,50), pos = (200,50))

        self.btnDigipot = wx.Button(self, label = "Send to Digipot", size = (80,50), pos = (310, 50))
        self.btnDigipot.Bind(wx.EVT_BUTTON, lambda event: self.toDigipot(wx.EVT_BUTTON, self.txtDigipot.GetValue()), self.btnDigipot)


    def toDigipot(self, event, valToWrite):

        try:
            print "hi"
            print valToWrite
            int(valToWrite)
            proc = subprocess.Popen("./i2cDigipot2 %s"%valToWrite, shell = True, stdout=subprocess.PIPE)

            for line in proc.stdout:
               print line


        except ValueError:
            print "Plese only input numbers"






print "done"
app = wx.App()
#window.Show(True)
myFrame(None)
app.MainLoop()


'''window = wx.Frame(None, title = "Frame", size = (500,500))
    panel = wx.Panel(window)
    '''

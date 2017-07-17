#wx Python
import wx

#to get/ send data through command line
import subprocess


#makes main window
class myFrame(wx.Frame):

    #constructor for window
    def __init__(self, *args, **kw):
        super(myFrame, self).__init__(*args, **kw)
        self.InitUI()


    #sets things up after constructor
    def InitUI(self):      
        
        self.SetSize((500,500))
        self.SetTitle("Frame")
        self.Show(True)

        #random label
        self.label = wx.StaticText(self, label = "Hello World", pos = (100,50))

        #text box for user to insert what to set digipot to
        self.txtDigipot = wx.TextCtrl(self, size =(100,50), pos = (200,50))

        #button to submit data in txtDigipot to digipot
        self.btnDigipot = wx.Button(self, label = "Send to Digipot", size = (80,50), pos = (310, 50))
        self.btnDigipot.Bind(wx.EVT_BUTTON, lambda event: self.toDigipot(wx.EVT_BUTTON, self.txtDigipot.GetValue()), self.btnDigipot)


    #writes to digipot and then reads to make sure changed.  result printed
    def toDigipot(self, event, valToWrite):

        try:
            int(valToWrite)
            proc = subprocess.Popen("./i2cDigipot2 %s"%valToWrite, shell = True, stdout=subprocess.PIPE)

            for line in proc.stdout:
               print line


        except ValueError:
            print "Plese only input numbers"






#sets up program
app = wx.App()
myFrame(None)
app.MainLoop()


'''*******************old unused code ****************************'''
#import sys

#print "started"

#print "hi"
#print valToWrite

#window.Show(True)
#print "done"


'''window = wx.Frame(None, title = "Frame", size = (500,500))
    panel = wx.Panel(window)
    '''

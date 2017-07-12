
"""

 
"""
 
 
 
import wx
import random
 
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt
 
class p1(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()
         
        self.canvas = FigureCanvas(self,-1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()
     
    def plot(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, '*-')
        self.canvas.draw()    
       
 
class TestFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(650,600), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        self.sp = wx.SplitterWindow(self)
        self.p1 = p1(self.sp)
        self.p2 = wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
         
        self.sp.SplitHorizontally(self.p1,self.p2,470)
 
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Wow")
         
        self.btnStart = wx.Button(self.p2,-1,"Start/Stop", size=(80,40),pos=(50,10))
        self.btnStart.Bind(wx.EVT_BUTTON,self.plot)
         
	self.txtDaqNum = wx.TextCtrl(self.p2, -1, pos=(160,10), size=(70,40))
	
        self.btnSubmit = wx.Button(self.p2,-1,"Submit", size=(80,40),pos=(240,10))
        self.btnSubmit.Bind(wx.EVT_BUTTON,self.submit)
        
        self.btnHi = wx.Button(self.p2,-1,"Hi", size=(40,40),pos=(500,10))
        self.btnHi.Bind(wx.EVT_BUTTON,self.hi)
         
    def hi(self,event):
        print "Hi"
 
    def submit(self,event):
        print "lorem ipsum"
 
    def plot(self,event):
        self.p1.plot()       
 
app = wx.App(redirect=False)
frame = TestFrame(None,"DAQ Data Chart")
frame.Show()
app.MainLoop()

"""
Mark Goldberg at EnerSys
Help from Mr. Brian Venus
 
"""
 
 
#import wx python 
import wx
import random

#import matplotlib stuff 
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt    

from collections import deque

global isPaused
isPaused = True

global timerInterval
timerInterval = 1000

global xLocations
xLocations = deque([])

global numPoints
numPoints=0

global data
data = deque([])

#main frame of program (whole interface including graph) 
class frame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(650,600), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

	#makes two panels, one for interface and one for graph
        self.sp = wx.SplitterWindow(self)
        self.graph = graph(self.sp)
        self.gui = wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
         
        self.sp.SplitHorizontally(self.graph,self.gui,470)
 
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("fghLJSDDGAKLJGSDLAJ")
         
	#starts or stops timer (timer goes off when add point)
        self.btnStart = wx.Button(self.gui,-1,"Start/Stop", size=(80,40),pos=(50,10))
        self.btnStart.Bind(wx.EVT_BUTTON,self.startStop)
         
	#text box to enter the number of DAQ attached
	self.txtDaqNum = wx.TextCtrl(self.gui, -1, pos=(160,10), size=(70,40))
	
	#submits number of daq's in the txtDaqNum
        self.btnSubmit = wx.Button(self.gui,-1,"Submit", size=(80,40),pos=(240,10))
        self.btnSubmit.Bind(wx.EVT_BUTTON,self.submit)
        
	#random button for testing
        self.btnHi = wx.Button(self.gui,-1,"Hi", size=(40,40),pos=(500,10))
        self.btnHi.Bind(wx.EVT_BUTTON,self.hi)

	#when timer goes off add points
	self.timer=wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.addPoint)
         
    #random test method
    def hi(self,event):
        print "Hi"
    
    #submits number of DAQ (or will when I add that)
    def submit(self,event):
        print "lorem ipsum"
 
    #plots graph
    def plot(self,event):
        self.graph.plot()  

    #when timer goes off
    def addPoint(self, event):
	print "timer off" 
	global xLocations
	global data
	global numPoints

	xLocations.append(numPoints)
	data.append(0)

	print data
	print xLocations

	numPoints += 1

	self.graph.plot()

    #starts or stops the timer
    def startStop(self,event):
	global isPaused
	global timerInterval

	if(isPaused):
        	self.timer.Start(timerInterval)
		isPaused = False
		print "start"   
	else:
		self.timer.Stop() 
		isPaused = True
		print "stop"


#the graph for DAQ data 
class graph(wx.Panel):

    global xLocations

    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()
         
        self.canvas = FigureCanvas(self,-1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()
     
    def plot(self):
        ''' plot some random stuff '''
        #data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)

	print data
	print xLocations

        ax.plot(xLocations, data, '*-')
        self.canvas.draw()    
   

#controlling code
app = wx.App(redirect=False)
frame = frame(None,"DAQ Data Chart")
frame.Show()
app.MainLoop()